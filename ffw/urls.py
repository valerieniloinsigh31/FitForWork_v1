from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ffw'),
    path('privacy/', views.privacy, name='privacy'),
    path('techniques/', views.techniques, name='techniques'),
    path('founder/', views.founder, name='founder'),
    path('tiers/', views.tiers, name='tiers'),
    path('nutrition_newsletter/', views.nutrition_newsletter, name='nutrition_newsletter')
]
