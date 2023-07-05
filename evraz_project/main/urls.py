from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('plan', views.plan, name='plan'),
    path('fact', views.fact, name='fact'),
    path('dashboard', views.dashboard, name='dashboard')
]
