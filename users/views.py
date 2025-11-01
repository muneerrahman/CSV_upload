from django.shortcuts import render
import csv
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ImportedUser
from .serializers import CSVUploadSerializer
from .tasks import process_csv_data

class UploadUserView(APIView):
    def post(self,request):
        serializer= CSVUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTPP_400_BAD_REQUEST)

        file= request.FILES['file']
        file_data = file.read().decode('utf-8')

        # Call Celery task asynchronously
        process_csv_data.delay(file_data)

        return Response({
            "message": "File received. Processing started in background."
        }, status=status.HTTP_202_ACCEPTED)
