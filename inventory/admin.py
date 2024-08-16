from django.contrib import admin
from django.utils.timezone import now
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


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
    list_display = ("product", "quantity", "administrative_unit")
    search_fields = ("product",)
    list_filter = ("quantity",)
    actions = ["show_all_items"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.session.get("show_all_items", False):
            queryset = queryset.exclude(quantity=0)
        return queryset

    def show_all_items(self, request, queryset):
        request.session["show_all_items"] = True
        self.message_user(
            request, "Now showing all items, including those with zero quantity."
        )

    show_all_items.short_description = _("Show all items")

    def changelist_view(self, request, extra_context=None):
        # Reset the session variable when the page is loaded normally
        if "action" not in request.POST:
            request.session["show_all_items"] = False
        return super().changelist_view(request, extra_context)


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


@admin.register(StockMovement)
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

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Update InventoryItem quantity
        inventory_item = obj.inventory_item
        if obj.movement_type == "in":
            inventory_item.quantity += obj.quantity
        else:
            inventory_item.quantity -= obj.quantity

        inventory_item.save()




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
