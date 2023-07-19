from django.urls import path
from core_api.endpoints import ArticuloListAPIView, BreakingNewsAPIView

urlpatterns = [
    path('articulos/', ArticuloListAPIView.as_view(), name='listado-articulos'),
    path('breaking-news/', BreakingNewsAPIView.as_view(), name='breaking-news'),
]

