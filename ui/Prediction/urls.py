from django.conf.urls import url
from . import  views

app_name = 'Prediction'

urlpatterns = [

    #Prediction/
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.results, name='index'),

    url(r'^results/', views.results, name='results'),

    #url(r'^results/', views.search_by_model, name='results'),

]

  
    
