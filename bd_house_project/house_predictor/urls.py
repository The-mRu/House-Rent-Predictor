from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('predict/', views.predict_page, name='predict_page'),
    path('predict_result/', views.predict_result, name='predict_result'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'), 

]



