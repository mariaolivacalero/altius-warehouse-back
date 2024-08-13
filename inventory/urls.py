from django.urls import path

from .views import category_views, product_views, inventory_item_views, administrative_unit_views, reception_batch_views

urlpatterns = [
    path('inventory-items/', inventory_item_views.item_list, name='inventory-items'),
    path('inventory-items/<int:pk>/', inventory_item_views.item_detail, name='inventory-items-detail'),
    path('products/', product_views.product_list, name='products'),
    path('products/<int:pk>/', product_views.product_detail, name='product-detail'),
    path('categories/', category_views.category_list, name='categories'),
    path('categories/<int:pk>/', category_views.category_detail, name='category-detail'),
    path('administrative_units', administrative_unit_views.administrative_unit_list, name='administrative_units'),
    path('administrative_units/<int:pk>/', administrative_unit_views.administrative_unit_detail, name='administrative_unit-detail'),
    path('reception-batches/', reception_batch_views.reception_batch_list, name='reception-batches'),
    path('reception-batches/<int:pk>/', reception_batch_views.reception_batch_detail, name='reception-batch-detail'),

]
