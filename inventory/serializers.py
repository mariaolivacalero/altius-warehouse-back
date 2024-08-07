from rest_framework import serializers
from .models import Supplier,Inventory, Product, ReceptionBatch, StockMovement 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'  # This includes the id

class InventoryItemSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()  # Nested serializer for Supplier

    class Meta:
        model = Inventory
        fields = '__all__'  # This includes the id

class  ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # This includes the id

class ReceptionBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionBatch
        fields = '__all__'  # This includes the id

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'  # This includes the id