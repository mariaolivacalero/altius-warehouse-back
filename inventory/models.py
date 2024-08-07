from django.db import models

# Create your models here.
from django.db import models
from custom_auth.models import User  # Assuming your custom user model is in custom_auth

class Product(models.Model):
    ean = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=50)

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    expiration_date = models.DateField(null=True, blank=True)
    lot_number = models.CharField(max_length=50, blank=True, null=True)
    # best_before_date = models.DateField(null=True, blank=True)

class ReceptionBatch(models.Model):
    receiving_date = models.DateField()
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    total_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    receiptID = models.CharField(max_length=50, unique=True)

class StockMovement(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=50)
    quantity = models.IntegerField()
    date = models.DateField()
    reason = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()  # Update with appropriate fields for contact info
