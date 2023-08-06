from django.contrib import admin
from django.urls import path
from .import views

app_name = 'moviedetail'

urlpatterns = [
    path('movie-details/',views.moviedetail, name='movie-details'),
    path('movie-details/<int:movieid>/',views.moviedetail,name='movie-details'),
    path('movie-details/<int:id>/',views.toprating,name='movie-details'),
]
