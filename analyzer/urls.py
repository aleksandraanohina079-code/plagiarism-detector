from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.check_text, name='check'),
    path('history/', views.history, name='history'),
]
