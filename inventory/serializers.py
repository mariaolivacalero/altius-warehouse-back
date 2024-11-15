from rest_framework import serializers
from .models import (
    AdministrativeUnit,
    Party,
    InventoryItem,
    Product,
    Reception,
    Batch,
    Category,
)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = "__all__"


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AdministrativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeUnit
        fields = "__all__"

# EAN lookup
class EANLookupSerializer(serializers.Serializer):
    ean = serializers.CharField(max_length=13, min_length=13)

    def validate_ean(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("EAN code must contain only numbers")
        return value