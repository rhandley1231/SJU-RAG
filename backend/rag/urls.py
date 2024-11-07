from django.urls import path
from .views import ask

urlpatterns = [
    path('rag-query/', ask, name='rag_query'),
]
