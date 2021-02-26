from django.urls import path, include
from . import views
from rest_framework import routers
from dashboard import views

router = routers.DefaultRouter()
router.register('file_upload', views.myFileConversion)
router.register('converted', views.myConvertedFile)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', views.index, name='index'),
    path('register',views.userRegistration, name='userRegistration'),
    path('login',views.authentication, name='userLogin'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('convert', views.convertfile, name='convert'),
    path('upload', views.uploadFile, name='uploadFile'),
    path('logout', views.logout, name='logout')
]