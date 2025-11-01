from django.shortcuts import render
import csv
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ImportedUser
from .serializers import CSVUploadSerializer

class UploadUserView(APIView):
    def post(self,request):
        serializer= CSVUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTPP_400_BAD_REQUEST)

        file= request.FILES['file']
        decoded_file=file.read().decode('utf-8').splitlines()
        reader=csv.DictReader(decoded_file)

        success_count= 0
        failed=[]

        for row in reader:
            name= row.get('name')
            email = row.get('email')
            age = int(row.get('age',-1))

            if not (name and email and 0 <= age <= 120):
                failed.append({"email":email,"reason":"invalid data"})
                continue
            if ImportedUser.objects.filter(email=email).exists():
                failed.append({"email":email,"reason":"Duplicate email"})
                continue

            ImportedUser.objects.create(name=name,email=email,age=age)
            success_count+=1

        return Response({
            "status": "Completed",
            "success count":success_count,
            "failed": failed
        })
