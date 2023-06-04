from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_plans, name='plans'),
    path('<plan_id>', views.plan_detail, name='plan_detail'),
]
