from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InvoiceDetailModel, InvoiceModel
from .serializers import InvoiceDetailModelSerializer, InvoiceModelSerializer
from rest_framework.exceptions import ValidationError

class InvoiceView(APIView):
    def post(self, request):
        try: 
            serializer = InvoiceModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response(
                {"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "An error occurred while creating the Invoice."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    def put(self, request, id):
        try:
            invoice_id = InvoiceModel.objects.get(id=id)
            serializer = InvoiceModelSerializer(invoice_id, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except InvoiceModel.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        except ValidationError as e:
            return Response(
                {"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {"error": "An error occurred while updating the invoice."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )