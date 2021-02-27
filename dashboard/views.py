from django.http import JsonResponse
from django.shortcuts import render
from .models import fileConversion, convertedFile
from django.core import serializers
from .forms import UserRegistrationForm, UploadFileForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
import convertapi
import os
import tempfile
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from .serializer import file_serializer, converted_fileserializer
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import wget
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import requests
from django_filters.rest_framework import DjangoFilterBackend





convertapi.api_secret = 'dpLCyj0liZqWEv4I'



class myFileConversion(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    queryset = fileConversion.objects.all()
    serializer_class = file_serializer
    filter_fields = ['user']

class myConvertedFile(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    queryset = convertedFile.objects.all()
    serializer_class = converted_fileserializer
    filter_fields = ['user']


def index(request):
    return render(request, 'home.html')


def userRegistration(request):
    if request.method=='POST':
        user = User(
            username = request.POST.get('username'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email')
        )
        user.set_password(request.POST.get('password'))
        user.is_active = True
        user.save()
        return redirect(index)
    return render(request, 'registration.html')

def authentication(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['logged_User']=[user.username, user.first_name, user.last_name, user.email]
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect(dashboard)
        else:
            return HttpResponse("Please Enter the correct Password")
    return render(request, 'login.html')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')

def getHost(request):
    host = request.get_host()
    if request.is_secure():
        return "https://{}".format(host)
    return "http://{}".format(host)

def convertfile(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename)
        upload_io = convertapi.UploadIO(open(f'media/{filename}', 'rb'))
        params = { 'File': upload_io, 'converter': 'openoffice' }
        saved_files = convertapi.convert('pdf', params).save_files(tempfile.gettempdir())
        print("The PDF saved to %s" % saved_files)
        return HttpResponse("file Uploaded")
    return render(request, 'upload.html')

@login_required(login_url='/login')
def uploadFile(request):
    form = UploadFileForm
    if request.user.is_authenticated:
        user = request.user
    if request.method == "POST":
        myform = UploadFileForm(request.POST, request.FILES)
        if myform.is_valid():
            if "from" in request.GET:
                _from = request.GET['from']
                _to = request.GET['to']
                newFile = myform.save()
                filename = newFile.myfile
                path = file_converter(_from,_to,filename)
            else:
                newFile = myform.save()
                filename = newFile.myfile
                upload_io = convertapi.UploadIO(open(f'media/{filename}', 'rb'))
                params = { 'File': upload_io, 'converter': 'openoffice' }
                c_file = convertapi.convert('pdf', params)
                path = c_file.save_files('media/')
            try:
                newData = convertedFile(
                    c_file=path[0], 
                    user=user
                )
                newData.save()
                print(newData.pk)
            except Exception as e:
                print(f"Problem: {e}")
            return render(request, 'upload_file.html', {'form':form,'uid':user.id, 'uploaded_to':path[0],'file_name':filename})
        return HttpResponse("something wrong")
    return render(request, 'upload_file.html', {'form':form,'uid':user.id})

def file_converter(_from, _to, file):
    c_file = convertapi.convert(f'{_to}', {
        'File': f'media/{file}'
    }, from_format = f'{_from}')
    path = c_file.save_files('media/')
    return path

@csrf_exempt
@api_view(['POST'])
def download_file(request):
    if request.method == "POST":
        try:
            c_id = request.data.get("c_id")
            data = convertedFile.objects.get(id=c_id)
            path = data.c_file
            url = getHost(request)+"/"+path
            print(url)
            wget.download(url)
            return HttpResponse("yes")
        except Exception as e:
            print(e)
            return HttpResponse("Something Wrong")
        

def logout(request):
    request.session.clear()
    return redirect(index)

