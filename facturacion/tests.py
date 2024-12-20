from django.test import TestCase, Client
from django.urls import reverse
import json

class ResumenDiarioTest(TestCase):
    def test_resumen_diario_post(self):
        # Define the URL for the API endpoint
        url = reverse('resumen_diario')  # Adjust this to match your URL pattern name if different

        # Example payload
        data = {
            'cabecera': {
                'tipo_comprobante': 'RC',
                'serie': '001',
                'correlativo': '00001',
                'fecha_referencia': '2024-08-20',
                'fecha_envio': '2024-08-21',
            },
            'emisor': {
                'ruc': '20123456789',
                'razon_social': 'Empresa S.A.C.',
            },
            'documentos': [
                {
                    'document_type_code': '03',
                    'id': 'B001-00000001',
                    'condition_code': '1',
                    'currency': 'PEN',
                    'total_amount': '100.00',
                    'paid_amount': '82.00',
                    'instruction_id': '01',
                    'tax_amount': '18.00',
                    'tax': [
                        {
                            'tax_amount': '18.00',
                            'id': '1000',
                            'name': 'IGV',
                            'tax_type_code': 'VAT',
                        },
                    ],
                },
            ],
        }

        # Send a POST request to the API endpoint
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, 200)  # Change to expected status code

        # Check the response content
        response_data = response.json()
        print(f"Response: {response_data}")

        # You can add further assertions here based on the expected response


class EmitirComprobanteTest(TestCase):
    def test_emitir_factura(self):
        # Define the URL for the API endpoint
        url = reverse('emitir_comprobante')  # Adjust this to match your URL pattern name if different

        # Prepare the data to send in the request
        factura_data = {
            "comprobante": {
                "serieDocumento": "F001",
                "numeroDocumento": "00012345",
                "fechaEmision": "2024-08-22",
                "DueDate": "2024-09-22",
                "tipoComprobante": "01",
                "cantidadItems": 1,
                "MontoTotalImpuestos": 30.51,
                "ImporteTotalVenta": 169.50,
                "totalConImpuestos": 200.01
            },
            "emisor": {
                "TipoDocumento": "6",
                "DocumentoEmisor": "20123456789",
                "RazonSocialEmisor": "Empresa SAC",
                "ubigeo": "150101",
                "calle": "Av. Siempre Viva 123",
                "distrito": "Lima",
                "provincia": "Lima",
                "departamento": "Lima"
            },
            "adquiriente": {
                "TipoDocumentoAdquiriente": "6",
                "NumeroDocumentoAdquiriente": "20605139293",
                "razonSocial": "Cliente Pérez",
                "CalleComprador": "Jr. Los Andes 456",
                "distritoComprador": "Miraflores",
                "provinciaComprador": "Lima",
                "departamentoComprador": "Lima"
            },
            "taxes": {
                "IGV": {
                    "operacionesGravadas": 169.50,
                    "MontoTotalImpuesto": 30.51,
                    "cod1": "1000",
                    "cod2": "IGV",
                    "cod3": "VAT",
                    "cod4": "S",
                    "afectacionIGV": '10',
                }
            },
            "Items": [
                {
                    "unidadMedida": "NIU",
                    "CantidadUnidadesItem": 2,
                    "totalValorVenta": 169.5,
                    "precioUnitarioConImpuestos": 100.005,
                    "tipoPrecio": "01",
                    "totalTax": 30.51,
                    "DescripcionItem": "Producto B",
                    "id": "PROD002",
                    "precioUnitario":84.75,
                    "tax": {
                        "IGV": {
                            "operacionesGravadas": 169.50,
                            "MontoTotalImpuesto": 30.51,
                            "cod1": "1000",
                            "cod2": "IGV",
                            "cod3": "VAT",
                            "afectacionIGV": '10',
                        }
                    }
                }
            ],
            "payTerms": [
        {
            "metodo": "contado",
        }
    ]
        }

        # Convert the data to JSON format
        json_data = json.dumps(factura_data)

        # Send a POST request to the API endpoint
        response = self.client.post(url, json_data, content_type='application/json')

        # Print the response content
        print(f"Response: {response.json()}")

        # Check the response status code
        self.assertEqual(response.status_code, 200)  # Adjust this if you expect a different status code

        
# data = {
#     'vendedor': 
#         {
#             "id": 6,
#             "numeroDocumento": "72184433",
#             "razonSocial": "Nury Marin",
#             "nombreComercial": "",
#             "celular": "987456123",
#             "direccion": "calle 11 se setiembre",
#             "imagen": "",
#             "tipoDocumento": "1",
#             "ubigeo": 1,
#             "codigoPais": 1
#         },
#         'adquiriente': 
#         {
#             "id": 6,
#             "numeroDocumento": "72184433",
#             "razonSocial": "Nury Marin",
#             "nombreComercial": "",
#             "celular": "987456123",
#             "direccion": "calle 11 se setiembre",
#             "imagen": "",
#             "tipoDocumento": "1",
#             "ubigeo": 1,
#             "codigoPais": 1
#         },
        
#         'comprobante':
#             {
#                 "emisor": 1,
#                 "adquiriente": 2,
#                 "tipoComprobante": ,
#                 "tipoOperacion":, 
#                 "tipoPago":,
#                 "serie":,
#                 "numeroComprobante":, 
#                 "fechaEmision":,
#                 "codigoMoneda":,
#                 "estado":,
#             }
            
#         items: {
#             {
#             "id": 3,
#             "nombre": "Articulo3",
#             "descripcion": "Articulo3",
#             "valorUnitario": 5,
#             "stock": 5,
#             "peso": 4.0,
#             "volumen": 3.0,
#             "unidadMedida": "4A",
#             "tipoPrecio": "01",
#             "codigoProducto": "1010152-",
#             "categoria": 10
#             'taxes': [
#                         {
#                 "porcentaje": null,
#                 "item": null,
#                 "impuesto": null,
#                 "afectacion": null
#             } ]
#         },
#         }
# }



        # Add further assertions here based on the expected response

    # def test_emitir_boleta(self):
    #     # Define the URL for the API endpoint
    #     url = reverse('emitir_comprobante')

    #     # Prepare the data to send in the request
    #     boleta_data = {
    #         "comprobante": {
    #             "serieDocumento": "B001",
    #             "numeroDocumento": "00056789",
    #             "fechaEmision": "2024-08-22",
    #             "DueDate": "2024-09-22",
    #             "tipoComprobante": "03",
    #             "cantidadItems": 1,
    #             "MontoTotalImpuestos": 36.00,
    #             "ImporteTotalVenta": 200.00,
    #             "totalConImpuestos": 236.00
    #         },
    #         "emisor": {
    #             "TipoDocumento": "6",
    #             "DocumentoEmisor": "20123456789",
    #             "RazonSocialEmisor": "Empresa SAC",
    #             "ubigeo": "150101",
    #             "calle": "Av. Siempre Viva 123",
    #             "distrito": "Lima",
    #             "provincia": "Lima",
    #             "departamento": "Lima"
    #         },
    #         "adquiriente": {
    #             "TipoDocumentoAdquiriente": "1",
    #             "NumeroDocumentoAdquiriente": "87654321",
    #             "razonSocial": "Cliente Gómez",
    #             "CalleComprador": "Av. Los Rosales 789",
    #             "distritoComprador": "San Isidro",
    #             "provinciaComprador": "Lima",
    #             "departamentoComprador": "Lima"
    #         },
    #         "taxes": {
    #             "IGV": {
    #                 "operacionesGravadas": 200.00,
    #                 "MontoTotalImpuesto": 36.00,
    #                 "cod1": "1000",
    #                 "cod2": "IGV",
    #                 "cod3": "VAT",
    #                 "cod4": "S"
    #             }
    #         },
    #         "Items": [
    #             {
    #                 "unidadMedida": "NIU",
    #                 "CantidadUnidadesItem": 2,
    #                 "totalValorVenta": 200.00,
    #                 "precioUnitarioConImpuestos": 118.00,
    #                 "tipoPrecio": "01",
    #                 "totalTax": 36.00,
    #                 "DescripcionItem": "Producto B",
    #                 "id": "PROD002",
    #                 "precioUnitario": 100.00,
    #                 "tax": {
    #                     "IGV": {
    #                         "operacionesGravadas": 200.00,
    #                         "MontoTotalImpuesto": 36.00,
    #                         "cod1": "1000",
    #                         "cod2": "IGV",
    #                         "cod3": "VAT",
    #                     }
    #                 }
    #             }
    #         ],
    #         "payTerms": [
    #     {
    #         "metodo": "contado"
    #     }
    # ]
    #     }

    #     # Convert the data to JSON format
    #     json_data = json.dumps(boleta_data)

    #     # Send a POST request to the API endpoint
    #     response = self.client.post(url, json_data, content_type='application/json')

    #     # Check the response status code
    #     self.assertEqual(response.status_code, 200)

    #     # Print the response content
    #     print(f"Response: {response.json()}")

    #     # Add further assertions here based on the expected response


class EmitirNotaCreditoTestCase(TestCase):
    def setUp(self):
        # Set up any initial data or configurations here if necessary
        self.client = Client()
        self.url = reverse('comunicado_bajas')  # Ensure this matches the URL pattern name in your urls.py

        # Example data for the test
        self.valid_data = {
            "comprobante": {
                "serieDocumento": "F001",
                "numeroDocumento": "123456",
                "fechaEmision": "2024-08-22",
                "MontoTotalImpuestos": "180.00",
                "ImporteTotalVenta": "1000.00",
                "totalConImpuestos": "1180.00"
            },
            "emisor": {
                "TipoDocumento": "6",  # RUC
                "DocumentoEmisor": "20123456789",
                "RazonSocialEmisor": "Empresa SAC",
                "ubigeo": "150101",
                "calle": "Av. Principal 123",
                "distrito": "Lima",
                "provincia": "Lima",
                "departamento": "Lima"
            },
            "adquiriente": {
                "TipoDocumentoAdquiriente": "1",  # DNI
                "NumeroDocumentoAdquiriente": "01234567",
                "razonSocial": "Juan Perez"
            },
            "taxes": {
                "IGV": {
                    "operacionesGravadas": "1000.00",
                    "MontoTotalImpuesto": "180.00",
                    "cod1": "1000",
                    "cod2": "IGV",
                    "cod3": "VAT",
                    "cod4": "S"
                }
            },
            "Items": [
                {
                    "unidadMedida": "NIU",
                    "CantidadUnidadesItem": "2",
                    "totalValorVenta": "1000.00",
                    "precioUnitarioConImpuestos": "590.00",
                    "tipoPrecio": "01",
                    "totalTax": "180.00",
                    "DescripcionItem": "Producto A",
                    "id": "A001",
                    "precioUnitario": "500.00",
                    "tax": {
                        "IGV": {
                            "operacionesGravadas": "1000.00",
                            "MontoTotalImpuesto": "180.00",
                            "cod1": "1000",
                            "cod2": "IGV",
                            "cod3": "VAT"
                        }
                    }
                }
            ],
            "documentoRelacionado": {
                "serieDocumento": "F001",
                "numeroDocumento": "654321",
                "tipoComprobante": "01"  # Factura
            }
        }

    def test_emitir_nota_credito_success(self):
        # Convert the data to JSON format
        json_data = json.dumps(self.valid_data)

        # Make the POST request to the API endpoint
        response = self.client.post(self.url, data=json_data, content_type='application/json')

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected success message
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Nota de Credito aceptada')

        print(f"Response: {response.json()}")
