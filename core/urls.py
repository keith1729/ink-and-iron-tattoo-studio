from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.booking_request, name='booking_request'),
    path('book/success/', views.booking_success, name='booking_success'),
    path('tattoos/', views.tattoo_gallery, name='tattoo_gallery'),
    path('artists/', views.artist_list, name='artist_list'),
]