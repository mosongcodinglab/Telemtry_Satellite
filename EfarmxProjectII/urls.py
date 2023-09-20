"""
URL configuration for EfarmxProjectII project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from EfarmAPP import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.map.as_view(), name='map'),
    path('MyField',views.MyField.as_view(),name='MyField'),
    path('Sentinel_Imagery',views.Sentinel_Imagery.as_view(),name='Sentinel_Imagery'),
    path('NDVI',views.NDVI.as_view(),name='NDVI'),
    path('EVI',views.EVI.as_view(),name='EVI'),
    path('NDWI',views.NDWI.as_view(),name='NDWI'),
    path('MSAVI',views.MSAVI.as_view(),name='MSAVI'),
    path('precipitation',views.precipitation.as_view(),name='precipitation'),
    path('Acres',views.Acres.as_view(),name='Acres'),
    path('Hectares',views.Hectares.as_view(),name='Hectares'),
    path('Kilometers',views.Kilometers.as_view(),name='Kilometers'),
    path('areameters',views.areameters.as_view(),name='areameters'),
    path('LandUseLandCover',views.LandUseLandCover.as_view(),name='LandUseLandCover'),
    path('Crop_Health',views.Crop_Health.as_view(),name='Crop_Health'),
    path('LST',views.LST.as_view(),name='LST'),
    path('True_Colour',views.True_Colour.as_view(),name='True_Colour'),
    path('False_Colour',views.False_Colour.as_view(),name='False_Colour'),

    path('ThreeD',views.ThreeD.as_view(),name='ThreeD'),
    path('soil_moisture',views.soil_moisture.as_view(),name='soil_moisture'),
    path('DEM',views.DEM.as_view(),name='DEM'),
    path('soiltype',views.soiltype.as_view(),name='soiltype'),
    path('Topograpic_Elevation',views.Topograpic_Elevation.as_view(),name='Topograpic_Elevation'),
    path('Bedrock',views.Bedrock.as_view(),name='Bedrock'),
    # path('areameters',views.areameters.as_view(),name='areameters'),
    # path('LandUseLandCover',views.LandUseLandCover.as_view(),name='LandUseLandCover'),
    


]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)