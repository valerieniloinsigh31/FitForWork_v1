from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_plans, name='plans'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('add/', views.add_plan, name='add_plan'),
    path('edit/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
]
