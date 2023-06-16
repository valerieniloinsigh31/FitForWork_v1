from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ffw'),
    path('privacy/', views.privacy, name='privacy')
]
