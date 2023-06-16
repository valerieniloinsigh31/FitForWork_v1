from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ffw'),
    path('privacy/', views.privacy, name='privacy'),
    path('techniques/', views.techniques, name='techniques'),
    path('founder/', views.founder, name='founder')
]
