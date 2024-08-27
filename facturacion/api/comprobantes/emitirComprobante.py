from lxml import etree as ET
import xmlsec
from django.http import JsonResponse
from facturacion.api.getpfx import extract_pfx_details
from facturacion.api.comprobantes.dxmlFromString import dxmlFromString
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import timedelta
from facturacion.api.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.api.modify_xml import modify_xml
from facturacion.api.xml_envio import envio_xml
from facturacion.api.exctractHashCode import extract_digest_value
import base64
import io
import os
import requests
import zipfile
import io
import json

def emitirComprobanteAPI(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        emisorDict = data['emisor']
        comprobanteDict = data['comprobante']
        
        # Generate file name
        fileName = f'{emisorDict["DocumentoEmisor"]}-{comprobanteDict["tipoComprobante"]}-{comprobanteDict["serieDocumento"]}-{comprobanteDict["numeroDocumento"]}.xml'
        
        # Construct the XML file path
        filePath = dxmlFromString(data, fileName)

        # Load the PFX certificate
        pfx_path = "facturacion/api/certificate/certificado.pfx"
        pfx_password = b'Jose_d@vid2004'

        with open(pfx_path, "rb") as pfx_file:
            pfx_data = pfx_file.read()

        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, pfx_password)
        
        # Modify XML (if necessary)
        modify_xml(filePath)
        
        # Encode the XML file as ZIP and Base64
        encodedZip = zip_and_encode_base64(filePath)
        
        # Send the XML file via SOAP request
        response = envio_xml(fileName, encodedZip, tipo=True)
        
        # Handle the SOAP response
        if response.status_code == 200:
            try:
                # Parse the XML response using lxml
                root = ET.fromstring(response.content)

                # Find the element that contains the base64 encoded content
                application_response_element = root.find('.//{*}applicationResponse')
                
                if application_response_element is not None:
                    # Decode the base64 content
                    decoded_content = base64.b64decode(application_response_element.text)

                    # Verify if the decoded content starts with the ZIP file signature
                    if decoded_content.startswith(b'PK'):
                        try:
                            # Create a BytesIO object to treat the bytes as a file
                            file_like_object = io.BytesIO(decoded_content)

                            # Open the ZIP file
                            with zipfile.ZipFile(file_like_object, 'r') as zip_ref:
                                # List all the contents in the ZIP file
                                zip_ref.printdir()

                                # Extract all the files to the specified directory
                                zip_ref.extractall('facturacion/api/response')

                                responseFile = ET.parse(f'facturacion/api/response/R-{fileName}')

                                namespaces = {'cbc' : 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}

                                response_code = responseFile.findtext('.//cbc:ResponseCode', namespaces=namespaces)
                                description = responseFile.findtext('.//cbc:Description', namespaces=namespaces)

                                # Return a success message as a JSON response
                                if response_code == '0':
                                    hashCode = extract_digest_value(filePath)
                                    return JsonResponse({'message': 'Comprobante aceptado', 'hash_code': str(hashCode)})
                                else:
                                    return JsonResponse({'error': f'{response_code}', 'descripcion': f'{description}'})
                        except zipfile.BadZipFile:
                            return JsonResponse({'error': 'The file is not a valid ZIP file.'}, status=400)
                    else:
                        return JsonResponse({'error': 'Decoded content does not appear to be a ZIP file.'}, status=400)
                else:
                    print(response.content)
                    return JsonResponse({'error': "applicationResponse element not found in the XML."}, status=500)
                
            except ET.XMLSyntaxError as e:
                return JsonResponse({'error': f"Failed to parse XML: {e}"}, status=500)
        else:
            print(response.content)
            return JsonResponse({'error': f"HTTP request failed with status code {response.status_code}"}, status=response.status_code)
    except Exception as e:
        print(e)