from rest_framework import serializers
from .models import AdministrativeUnit, Supplier,InventoryItem, Product, ReceptionBatch, StockMovement, Category 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__' 

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__' 

class  ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 

class ReceptionBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionBatch
        fields = '__all__' 

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__' 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AdministrativeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeUnit
        fields = '__all__'