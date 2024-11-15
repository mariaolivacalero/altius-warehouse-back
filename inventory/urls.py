from django.urls import path

from .views import (
    batch_views,
    category_views,
    product_views,
    inventory_item_views,
    administrative_unit_views,

)

urlpatterns = [
    path("inventory-items/", inventory_item_views.item_list, name="inventory-items"),
    path(
        "inventory-items/<int:pk>/",
        inventory_item_views.item_detail,
        name="inventory-items-detail",
    ),
    path("products/", product_views.product_list, name="products"),
    path("products/<int:pk>/", product_views.product_detail, name="product-detail"),
    path("categories/", category_views.category_list, name="categories"),
    path(
        "categories/<int:pk>/", category_views.category_detail, name="category-detail"
    ),
    path(
        "administrative_units",
        administrative_unit_views.administrative_unit_list,
        name="administrative_units",
    ),
    path(
        "administrative_units/<int:pk>/",
        administrative_unit_views.administrative_unit_detail,
        name="administrative_unit-detail",
    ),
    path("batches/", batch_views.batch_list, name="batches"),
    path("batches/<int:pk>/", batch_views.batch_detail, name="batch-detail"),
    path('ean-lookup/', product_views.ean_lookup, name='ean_lookup'),

]
