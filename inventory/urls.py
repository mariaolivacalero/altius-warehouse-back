from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.item_list, name='inventory'),
    path('inventory/<int:pk>/', views.item_detail, name='inventory-detail'),
    path('products', views.product_list, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    
]