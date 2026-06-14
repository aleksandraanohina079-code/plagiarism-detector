from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.corpus_list, name='corpus_list'),
    path('doc/<int:doc_id>/', views.document_detail, name='document_detail'),
]
