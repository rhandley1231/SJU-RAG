from django.urls import path
from .views import rag_query

urlpatterns = [
    path('rag-query/', rag_query),
]
