from django.urls import path
from . import views

urlpatterns=[
    path('',views.place_list, name='place_list'), # place list url path 
    path('visited', views.places_visited, name='places_visited'), #places visited url path
    path('place/<int:place_pk>/was visited', views.place_was_visited, name ='place_was_visited'), 
    path('about', views.about, name='about') #about url path 
    
]