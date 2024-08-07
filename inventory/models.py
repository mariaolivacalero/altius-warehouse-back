from django.db import models
from custom_auth.models import User  # Assuming your custom user model is in custom_auth

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    ean = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit_of_measure = models.CharField(max_length=50)

class Location(models.Model):
    name = models.CharField(max_length=255)

class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reception_batch = models.ForeignKey('ReceptionBatch', on_delete=models.CASCADE)  # Changed to CASCADE
    quantity = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateField(null=True, blank=True)
    lot_number = models.CharField(max_length=50, blank=True, null=True)

class ReceptionBatch(models.Model):
    receiving_date = models.DateField()
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)  # Changed to CASCADE
    total_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    receiptID = models.CharField(max_length=50, unique=True)

class StockMovement(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)  # Renamed for clarity
    movement_type = models.CharField(max_length=50, choices=[('in', 'In'), ('out', 'Out'), ('transfer', 'Transfer')])
    quantity = models.IntegerField()
    date = models.DateField()
    reason = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reception_batch = models.ForeignKey(ReceptionBatch, on_delete=models.SET_NULL, null=True, blank=True)

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(default="")
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
