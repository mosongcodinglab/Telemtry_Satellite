from django.shortcuts import render
from django.views.generic import TemplateView 


#Importation of variAous Libraries or packages...
from os import path as op
import geemap
import ee
import folium
import geemap.foliumap as geemap
import matplotlib.pyplot as plt
from django.http import HttpResponse
from folium import plugins
from folium.plugins import Draw

from .forms import DateForm
from datetime import datetime


#importing models:
from .models import fields

start_date="2020-01-01"#Set start_date(yy/mon/day)
end_date="2020-03-31"#Set End_date(yy/mon/day)

# Create your views here.        
#HomeMap
class map(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        ee.Initialize()
        ee.Authenticate()
        
        
        Map = geemap.Map()
        Map.add_to(figure)
        Map.set_center(-7.799, 53.484, 7)
        
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
 

        global basemaps
        basemaps = {
        'Google Maps': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Maps',
                overlay = False,
                control = True
                ),
                'Esri Satellite': folium.TileLayer(
                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr = 'Esri',
                name = 'Esri Satellite',
                overlay = True,
                control = True
                ),'Google Satellite Hybrid': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = False,
                control = True
                ), 
                }     
        basemaps['Google Satellite Hybrid'].add_to(Map)
        basemaps['Esri Satellite'].add_to(Map)
             
        Map.add_child(folium.LayerControl())
        figure.render()
        context['map'] = figure
        return context
    
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

                    
#ROI: MyField
class MyField(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
 
        global boundary
        boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")
        Map.center_object(boundary,10);
        Map.addLayer(boundary,{},"MyField")   
             
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['MyField'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

def indices(TemplateView):
    return render(request="index.html")

# class Sentinel_Imagery(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(request):
#         try:
#             figure = folium.Figure()
#             Map = geemap.Map()
#             Map.add_to(figure)
#         #     sss
#             # Rest of the code...

#             figure.render()
            
#             dddd
#             return {"Sentinel_Imagery": figure}

#         except Exception as e:
#             error_message = f"An error occurred: {e}"
#             return {"errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr": error_message}

    # Rest of the code...



#Sentinel Data.
class Sentinel_Imagery(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                global boundary
                # boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/IreLand")
                boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")

                Map.addLayer(boundary,{},"Boundary")
        
                Map.center_object(boundary,10);
                
                global season
                season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)
 #-------------SENTINEL_2A DATA----------------------#  
                global sentinel_2A
                sentinel_2A = ee.ImageCollection('COPERNICUS/S2')\
               .filterBounds(boundary)\
               .filter(season)\
               .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",10))\
               .median()\
               .select('B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B10', 'B11')\
               .clip(boundary)
                
                sentinel_2Avispar={"min":0, "max":4000,"bands": ['B4','B3','B2']}#Visualization parameters used.

                Map.addLayer(sentinel_2A,sentinel_2Avispar,"Sentinel Imagery")
                
                Map.add_child(folium.LayerControl())
                
                figure.render()
                return{"Sentinel_Imagery": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
#Normalized Difference Vegetation Index: NDVI.
class NDVI(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        plugin_Draw = True
                        )
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
        
                Map.centerObject(boundary,10)
      
                global NDVI
                NDVI = sentinel_2A.normalizedDifference(['B8', 'B4'])#normalized difference is computed as (first − second) / (first + second).
                ndvivis_parametres = {'min':0, 'max':1, 'palette': ['red','brown','yellow', 'green'] }#NDVI visualization parameters
                Map.addLayer(NDVI, ndvivis_parametres, 'Crop Helath-Analysis I')#Add Normalized Difference Vegetation Index to the layers
                
                NDVI_values = NDVI.reduceRegion(reducer=ee.Reducer.toList(), geometry=boundary, scale=10)

        # Convert NDVI values to a list
                NDVI_list = ee.List(NDVI_values.get('nd'))
                     # Convert NDVI list to a Python list
                NDVI_list_py = NDVI_list.getInfo()

                # Print the NDVI values
                print('NDVI values:', NDVI_list_py)
                
                vis_params = {
                    'min': 0,
                    'max': 1,
                    'palette':['red','brown','yellow', 'green'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Crop Health Analysis')
                legend_dict = {
                       'Non-crops(0 to 0.18)': 'FF0000',
                       'Unhealthly crops(0.18 to 0.41)': 'A52A2A',
                       'Moderately healthy crops(0.41 to 0.0.69)': 'FFFF00',
                       'Very healthy crops(0.69 to 1.0)': '008000',}
                Map.add_legend(title="NDVI Legend", legend_dict=legend_dict)
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"NDVI": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
#LandUseLandCover.
class LandUseLandCover(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        plugin_Draw = True
                        )
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.centerObject(boundary,10)
                
                                # Create a Sentinel-2 image composite
                # image = geemap.dynamic_world_s2(boundary, start_date, end_date)
                # vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
                # Map.addLayer(image, vis_params, 'Sentinel-2 image')
                
                # Create Dynamic World land cover composite
                landcover = geemap.dynamic_world(boundary, start_date, end_date, return_type='hillshade')
                Map.addLayer(landcover.clip(boundary), {}, 'Land Cover')
                # Add legend to the map
                Map.add_legend(title="Land Cover", builtin_legend='Dynamic_World')
                
      
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"LandUseLandCover": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
            
#Enhanced Vegetation Index: EVI.
class EVI(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.center_object(boundary,10);
                EVI = sentinel_2A.expression(
                    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                        'NIR' : sentinel_2A.select('B8').divide(10000),
                        'RED' : sentinel_2A.select('B4').divide(10000),
                        'BLUE': sentinel_2A.select('B2').divide(10000)})
                EVI_vispar={'min':-1, 'max':1, 'palette': ['yellow', 'brown','green']}#EVI visualization parameters
                Map.addLayer(EVI,EVI_vispar,"EVI(Enhanced Vegetation Index)")#Add Enhanced Vegetation Index to the layers
                
                
                vis_params = {
                    'min': 0,
                    'max': 1,
                    'palette':['yellow', 'brown','green'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='EVI')
                
                legend_dict = {
                    'Non-crops': '1D26B3',
                    'Unhealthly crops': 'F51294',
                    'Moderately healthy crops': '020206',
                    'Very healthy crops': '008000',}                
                Map.add_legend(title="EVI Legend", legend_dict=legend_dict)
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"EVI": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
            
#NDWI(Normalized Difference Water Index).
class NDWI(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.center_object(boundary,10);
                global NDWI
                NDWI = sentinel_2A.normalizedDifference(['B3', 'B11'])
                ndwivis_parametres = {min:-1, max:1, 'palette':  ['yellow','white', 'green','blue']}#NDWI visualization parameters
                Map.addLayer(NDWI, ndwivis_parametres,"NDWI( Normalized Difference Water Index)")#Add Normalized Difference Water Index to the layers
                vis_params = {
                        'min': -1,
                        'max': 1,
                        'palette':['yellow','white', 'green','blue'],
                    }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='NDWI')                
                
                legend_dict = {
                   'Non-aqueous surfaces(-1 to -0.3)': 'D9EE08',
                   'Moderate aqueous surfaces(-0.3 to 0.0)': 'FFFFFF',
                   'Flooding, humidity(0.0 to 0.2)': '08EE2F',
                   'Water surface(0.2 to 1.0)': '0836EE',}
                Map.add_legend(title="NDWI Legend", legend_dict=legend_dict)

                Map.add_child(folium.LayerControl())
                figure.render()
                return{"NDWI": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
                       
#MSAVI(Modified Soil-Adjusted Vegetation Index)
class MSAVI(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.center_object(boundary,10);        
                composite= sentinel_2A.divide(10000)
                msavi2 = composite.select('B8').multiply(2).add(1) \
                .subtract(composite.select('B8').multiply(2).add(1).pow(2) \
                        .subtract(composite.select('B8').subtract(composite.select('B4')).multiply(8)).sqrt()).divide(2)
                
                msavi2_vispar={'min':-1, 'max':1, 'palette': ['yellow', 'brown','green']}#MSAVI visualization parameters
                Map.addLayer(msavi2,msavi2_vispar,  'MSAVI(Modified Soil-Adjusted Vegetation Index)')#Add Modified Soil-Adjusted Vegetation Index to the layers
                vis_params = {
                'min': -1,
                'max': 0.6,
                'palette':['yellow', 'brown','green'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='MSAVI')                    
                legend_dict = {
                'Bare Soil(-1 to 0.2)': 'FFFF00',
                'Seed Germination Stage(0.2 to 0.4)': 'A52A2A',
                'Leaf Development Stage(0.4 to 0.6)': '40EE08',
                }
                Map.add_legend(title="MSAVI Legend",legend_dict=legend_dict)                   
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"MSAVI": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
            
#Precipitation.
class precipitation(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                 #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.center_object(boundary,10);
                dataset = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .filter(ee.Filter.date('2015-01-01', '2020-12-01'))\
                .mean()\
                .clip(boundary)

                global precipitation
                precipitation = dataset.select('precipitation')

                precipitationVis = {
                'min': 1,
                'max': 17,
                'palette': ['001137','0aab1e','e7eb05','ff4a2d','e90000'],
                }

                Map.addLayer(precipitation, precipitationVis, 'Precipitation')
                Rainfallvis_params = {
                'min': 1,
                'max': 17,
                'palette':['001137','0aab1e','e7eb05','ff4a2d','e90000'],
                }
                colors = Rainfallvis_params['palette']
                vmin = Rainfallvis_params['min']
                vmax = Rainfallvis_params['max']
                Map.add_colorbar(Rainfallvis_params,label='Precipitation')                    
                legend_dict = {
                'Heavy Precipitation': '001137',
                'Moderate Precipitation': '0aab1e',
                'Light Precipitation': 'e7eb05',
                'Trace Precipitation:': 'e90000'
                
                }
                Map.add_legend(title="Precipitation Legend",legend_dict=legend_dict)  
                
                
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"precipitation": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        
            
#NAN(NAN).
class nan(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        )
                Map.add_to(figure)
                Map.center_object(boundary,10);
                
             
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"nan": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
                        

# Area Estimation: Meters
class areameters(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")
        Map.center_object(boundary,10);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated crop areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['areameters'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)


# Area Estimation: Acres
class Acres(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")
        Map.center_object(boundary,10);
        Map.addLayer(boundary,{},"MyField") 
         
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(4046.86).round()
        print('Estimated crop areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Acres'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Hectares
class Hectares(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")
        Map.center_object(boundary,10);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(10000).round()
        print('Estimated crop areas(Hectares)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Hectares'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Kilometers
class Kilometers(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")
        Map.center_object(boundary,10);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(1000000).round()
        print('Estimated crop areas(KM)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Kilometers'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
        
#True_Colour.
class True_Colour(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.center_object(boundary,10);
                
                sentinel_2Avispar={"min":0, "max":4000,"bands": ['B4','B3','B2']}#Visualization parameters used.
                Map.addLayer(sentinel_2A,sentinel_2Avispar,"sentinel 2A: True Color")
                
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"True_Colour": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
            
#False_Colour.
class False_Colour(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                global boundary
                # boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/IreLand")
                boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")

                Map.addLayer(boundary,{},"Boundary")
        
                Map.center_object(boundary,10);
        
                sentinel_2Avispar={"min":0, "max":4000,"bands": ['B8','B4','B3']}#NIR, Red, Green.

                Map.addLayer(sentinel_2A,sentinel_2Avispar,"sentinel2A:false Color")
                
                Map.add_child(folium.LayerControl())
                
                figure.render()
                return{"False_Colour": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
      
        
#Crop Health(Dense Vegetation Bands B11,B8,B2)
class Crop_Health(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                global boundary
                boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")

                Map.addLayer(boundary,{},"Boundary")
        
                Map.center_object(boundary,10);
        
                sentinel_2Avispar={"min":0, "max":4000,"bands": ['B11','B8','B2']}#Crop Health(Dense Vegetation Bands B11,B8,B2)
                Map.addLayer(sentinel_2A,sentinel_2Avispar,"sentinel2A:false Color")
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"Crop_Health": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
        
                    
#Normalized Difference Vegetation Index: NDVI.
class LandUseLandCover(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        plugin_Draw = True
                        )
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.centerObject(boundary,10)
                
                                # Create a Sentinel-2 image composite
                # image = geemap.dynamic_world_s2(boundary, start_date, end_date)
                # vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
                # Map.addLayer(image, vis_params, 'Sentinel-2 image')
                
                # Create Dynamic World land cover composite
                landcover = geemap.dynamic_world(boundary, start_date, end_date, return_type='hillshade')
                Map.addLayer(landcover.clip(boundary), {}, 'Land Cover')
                # Add legend to the map
                Map.add_legend(title="Land Cover", builtin_legend='Dynamic_World')
                
      
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"LandUseLandCover": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
        
            
# LST(Land Surface Temperature)
class LST(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        plugin_Draw = True
                        )
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.centerObject(boundary,10)
                
                col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
                .filterDate('2013-01-01','2013-12-31') \
                .filterBounds(boundary)


                #imagen reduction
                image = col.mean().clip(boundary)
                # print(image, 'image')
                # Map.addLayer(image, vizParams2)


                #select thermal band 10(with brightness tempereature), no calculation
                thermal= image.select('B10').multiply(0.1)
                b10Params = {'min':291.918, 'max':302.382, 'palette': ['red','brown','yellow', 'green'] }#LST visualization parameters

                Map.addLayer(thermal, b10Params, 'thermal')
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"LST": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)


# soil moisture
class soil_moisture(TemplateView):
        template_name = 'index.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map(
                        plugin_Draw = True
                        )
                Map.add_to(figure)
                #mouse position
                fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
                plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
                # GPS
                plugins.LocateControl().add_to(Map)
                #Add measure tool 
                plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        
                Map.centerObject(boundary,10)
                
                dataset = ee.ImageCollection('NASA/SMAP/SPL3SMP_E/005') \
                                .filter(ee.Filter.date('2017-04-01', '2017-04-30'))\
                                        .mean()\
                                                .clip(boundary)

                soilMositureSurface = dataset.select('soil_moisture_am')
                soilMositureSurfaceVis = {
                'min': 0.0,
                'max': 0.6,
                'palette': ['0300ff', '418504', 'efff07', 'efff07', 'ff0303'],
                }
                Map.addLayer(soilMositureSurface, soilMositureSurfaceVis, 'Soil Mositure')
                
                
            
                colors = soilMositureSurfaceVis['palette']
                vmin = soilMositureSurfaceVis['min']
                vmax = soilMositureSurfaceVis['max']
                Map.add_colorbar(soilMositureSurfaceVis,label='Average Soil Temperature')                    
                legend_dict = {
                'Heavy Precipitation': '0300ff',
                'Moderate Precipitation': '418504',
                'Light Precipitation': 'efff07',
                'Trace Precipitation:': 'ff0303'
                
                }
                Map.add_legend(title="Precipitation Legend",legend_dict=legend_dict)  

                Map.add_child(folium.LayerControl())
                figure.render()
                return{"soil_moisture": figure}
        def get(self, request, pk=''):
                form = DateForm()
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
    
        def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)













###########################################################################################################
####Terrain Analysis:
###########################################################################################################
# 3DAnalysis:
class ThreeD(TemplateView):
        template_name = 'ThreeD.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                Map.set_center(-7.799, 53.484, 7)
                
                basemaps = {
                        'Google Maps': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Maps',
                                                overlay = False,
                                                control = True
                                        ),
                                                'Esri Satellite': folium.TileLayer(
                                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                attr = 'Esri',
                                                name = 'Esri Satellite',
                                                overlay = True,
                                                control = True
                                        ),'Google Satellite Hybrid': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Satellite',
                                                overlay = False,
                                                control = True
                                        ),
                
                }     
                basemaps['Google Satellite Hybrid'].add_to(Map)
                basemaps['Esri Satellite'].add_to(Map)
                
        
        
                Map.add_child(folium.LayerControl())
        
                figure.render()
        
                return{"ThreeD": figure}
                

# DEM(Digital Elevation ):
class DEM(TemplateView):
        template_name = 'DEM.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                Map.set_center(-7.799, 53.484, 7)
                
                basemaps = {
                        'Google Maps': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Maps',
                                                overlay = False,
                                                control = True
                                        ),
                                                'Esri Satellite': folium.TileLayer(
                                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                attr = 'Esri',
                                                name = 'Esri Satellite',
                                                overlay = True,
                                                control = True
                                        ),'Google Satellite Hybrid': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Satellite',
                                                overlay = False,
                                                control = True
                                        ),
                
                }     
                basemaps['Google Satellite Hybrid'].add_to(Map)
                basemaps['Esri Satellite'].add_to(Map)
                
                
                srtm=ee.Image("USGS/SRTMGL1_003")
                elev = srtm.select('elevation');
                # Get slope
                slope = ee.Terrain.slope(elev);

                # Clip Srtm DEM by geometry
                DEM_slope= slope.clip(boundary);
                slope_palette1 = ['0C7600','4CE500','B2FF18','FFFF00','FFAE00','ff6d66','FF0000']
                Map.addLayer(DEM_slope,{'palette':slope_palette1},"Digital Elevation Model")
                
                vis_params = {
                    'min': 0,
                    'max': 7000,
                    'palette':['0C7600','4CE500','B2FF18','FFFF00','FFAE00','ff6d66','FF0000'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Digital Elevation Model(DEM)')
                legend_dict = {
                       'Lowland (Up to 200 M)': '0C7600',
                       'Mountainous Areas: (Up to 500 M)': '4CE500',
                       'High Plateaus:(Around 2,000 M)': 'B2FF18',
                       'Extreme Elevations(Over 5000 M)': 'FF0000',}
                Map.add_legend(title="DEM Legend", legend_dict=legend_dict)
                
        
                Map.add_child(folium.LayerControl())
        
                figure.render()
        
                return{"DEM": figure}


#Soil Type
class soiltype(TemplateView):
        template_name = 'ThreeD.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                Map.set_center(-7.799, 53.484, 7)
                
                basemaps = {
                        'Google Maps': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Maps',
                                                overlay = False,
                                                control = True
                                        ),
                                                'Esri Satellite': folium.TileLayer(
                                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                attr = 'Esri',
                                                name = 'Esri Satellite',
                                                overlay = True,
                                                control = True
                                        ),'Google Satellite Hybrid': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Satellite',
                                                overlay = False,
                                                control = True
                                        ),
                
                }     
                basemaps['Google Satellite Hybrid'].add_to(Map)
                basemaps['Esri Satellite'].add_to(Map)
                
                boundary = ee.FeatureCollection("users/MosongJrn/KSA_Study_Area_Projected")

                dataset = ee.ImageCollection('NASA/SMAP/SPL3SMP_E/005') \
                                .filter(ee.Filter.date('2017-04-01', '2017-04-30'))\
                .mean()\
                # .clip(boundary)

                soilMositureSurface = dataset.select('soil_moisture_am')
                soilMositureSurfaceVis = {
                'min': 0.0,
                'max': 0.6,
                'palette': ['0300ff', '418504', 'efff07', 'efff07', 'ff0303'],
                }
                Map.centerObject(boundary,12)
                Map.addLayer(soilMositureSurface, soilMositureSurfaceVis, 'Soil Mositure')
        
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"soiltype": figure}
        
        



#Bedrock
class Bedrock(TemplateView):
        template_name = 'ThreeD.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                Map.set_center(-7.799, 53.484, 7)
                
                basemaps = {
                        'Google Maps': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Maps',
                                                overlay = False,
                                                control = True
                                        ),
                                                'Esri Satellite': folium.TileLayer(
                                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                attr = 'Esri',
                                                name = 'Esri Satellite',
                                                overlay = True,
                                                control = True
                                        ),'Google Satellite Hybrid': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Satellite',
                                                overlay = False,
                                                control = True
                                        ),
                
                }     
                basemaps['Google Satellite Hybrid'].add_to(Map)
                basemaps['Esri Satellite'].add_to(Map)
                
                dataset = ee.Image('NOAA/NGDC/ETOPO1')
                elevation = dataset.select('bedrock')
                elevationVis = {
                'min': -7000.0,
                'max': 3000.0,
                'palette': ['011de2', 'afafaf', '3603ff', 'fff477', 'b42109'],
                }
                Map.setCenter(-37.62, 25.8, 2)
                Map.addLayer(elevation, elevationVis, 'Elevation')
                
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"Bedrock": figure}
        

#Topograpic_Elevation
class Topograpic_Elevation(TemplateView):
        template_name = 'ThreeD.html'
        def get_context_data(request):
                figure = folium.Figure()
                Map = geemap.Map()
                Map.add_to(figure)
                Map.set_center(-7.799, 53.484, 7)
                
                basemaps = {
                        'Google Maps': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Maps',
                                                overlay = False,
                                                control = True
                                        ),
                                                'Esri Satellite': folium.TileLayer(
                                                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                attr = 'Esri',
                                                name = 'Esri Satellite',
                                                overlay = True,
                                                control = True
                                        ),'Google Satellite Hybrid': folium.TileLayer(
                                                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                attr = 'Google',
                                                name = 'Google Satellite',
                                                overlay = False,
                                                control = True
                                        ),
                
                }     
                basemaps['Google Satellite Hybrid'].add_to(Map)
                basemaps['Esri Satellite'].add_to(Map)
                
                srtm=ee.Image("USGS/SRTMGL1_003")

                lines = ee.List.sequence(0, 4000, 200)

                
                def func_pad(line):
                        mycontour = srtm \
                                .convolve(ee.Kernel.gaussian(5, 3)) \
                                .subtract(ee.Image.constant(line)).zeroCrossing() \
                                .multiply(ee.Image.constant(line)).toFloat()
                        return mycontour.mask(mycontour)

                contourlines = lines.map(func_pad)

                contourlines = ee.ImageCollection(contourlines).mosaic()

                Map.addLayer(contourlines, {'min': 0, 'max': 5000, 'palette':['00ff00', 'ff0000']}, 'contours')
                
                
                Map.add_child(folium.LayerControl())
                figure.render()
                return{"Topograpic_Elevation": figure}