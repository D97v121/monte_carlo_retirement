from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scenarios/', views.scenario_list, name='scenario_list'),
    path("api/simulate/", views.api_simulate, name="api_simulate"),
]
