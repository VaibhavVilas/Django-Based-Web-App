from django.urls import path
from Csv_App import views

urlpatterns = [
    path('', views.home, name='home')
]
