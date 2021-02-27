from rest_framework import serializers
from django.contrib.auth.models import User
from dashboard.models import fileConversion, convertedFile

class file_serializer(serializers.ModelSerializer):
    class Meta:
        model = fileConversion
        fields = ('myfile', 'user','created_on')

class converted_fileserializer(serializers.ModelSerializer):
    class Meta:
        model = convertedFile
        fields = ('c_file','user','created_on')
