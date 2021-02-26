from django.contrib import admin
from .models import fileConversion, convertedFile

class fileConvert(admin.ModelAdmin):
    pass

class convertFile(admin.ModelAdmin):
    pass

admin.site.register(fileConversion, fileConvert)
admin.site.register(convertedFile, convertFile)

