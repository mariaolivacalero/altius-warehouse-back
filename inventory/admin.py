from django.contrib import admin
from .models import (
    AdministrativeUnit,
    Category,
    InventoryItem,
    Location,
    Product,
    ReceptionBatch,
    StockMovement,
    Supplier,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("product", "administrative_unit", "quantity")
    search_fields = ("product", "administrative_unit")
    list_filter = ("administrative_unit",)

    def save_model(self, request, obj, form, change):
        # Pass the current user when saving the object
        obj.save(user=request.user)


@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category")
    search_fields = ("name", "code")
    list_filter = ("category",)


@admin.register(ReceptionBatch)
class ReceptionBatchAdmin(admin.ModelAdmin):
    list_display = (
        "receiving_date",
        "supplier",
        "total_quantity",
        "notes",
        "receiptID",
    )
    search_fields = ("receiving_date",)
    list_filter = ("receiving_date",)


# @admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_item",
        "movement_type",
        "quantity",
        "date",
        "user",
    )

    def inventory_item(self, obj):
        return obj.inventory_item.product.name if obj.inventory_item else None

    inventory_item.short_description = "Product Name"


admin.site.register(StockMovement, StockMovementAdmin)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")
    search_fields = ("name",)


# add Location
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("administrative_unit", "type")
    search_fields = ("administrative_unit", "type")
    list_filter = ("administrative_unit",)
