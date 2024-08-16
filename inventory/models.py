from django.db import models
from custom_auth.models import User  # Assuming your custom user model is in custom_auth
from django.db import IntegrityError
from django.utils.timezone import now
import hashlib


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=13, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    manufacturer = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=50)

    def generate_code(self):
        # Get the current date and time in YYYYMMDD-HHMMSS format
        timestamp = now().strftime("%Y%m%d%H%M%S")

        # Create a name prefix
        name_prefix = (self.manufacturer[:4].upper()).ljust(4, "X")

        # Create a unique string including the timestamp
        unique_string = (
            f"{self.name}-{self.category_id}-{self.manufacturer}-{timestamp}"
        )

        # Generate a hash and truncate it
        hash_part = hashlib.sha256(unique_string.encode()).hexdigest()[:6]

        return f"{name_prefix}{hash_part}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        # Handle possible IntegrityError in case of duplicate codes
        while True:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                # If there's a duplicate, generate a new code and try again
                self.code = self.generate_code()

    def __str__(self):
        return self.name


class AdministrativeUnit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{str(self.id)} - {self.name}"


class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reception_batch = models.ForeignKey(
        "ReceptionBatch", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    administrative_unit = models.ForeignKey(
        AdministrativeUnit, on_delete=models.SET_NULL, null=True
    )
    expiration_date = models.DateField(null=True, blank=True)
    lot_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.reception_batch.supplier} - {self.reception_batch.receiving_date}"

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # New InventoryItem logic
            warehouse_location = Location.objects.filter(
                administrative_unit=self.administrative_unit, type="warehouse"
            ).first()

            if warehouse_location:
                StockMovement.objects.create(
                    inventory_item=self,
                    movement_type="in",
                    location=warehouse_location,
                    quantity=self.quantity,
                    date=now().date(),
                    user=user,
                )

    def add_stock(self, quantity, user=None):
        self.quantity += quantity
        self.save()
        warehouse_location = Location.objects.filter(
            administrative_unit=self.administrative_unit, type="warehouse"
        ).first()
        if warehouse_location:
            StockMovement.objects.create(
                inventory_item=self,
                movement_type="in",
                location=warehouse_location,
                quantity=quantity,
                date=now().date(),
                user=user,
            )

    def remove_stock(self, quantity, user=None):
        if self.quantity < quantity:
            raise ValidationError("Cannot remove more stock than available.")
        self.quantity -= quantity
        self.save()
        warehouse_location = Location.objects.filter(
            administrative_unit=self.administrative_unit, type="warehouse"
        ).first()
        if warehouse_location:
            StockMovement.objects.create(
                inventory_item=self,
                movement_type="out",
                location=warehouse_location,
                quantity=quantity,
                date=now().date(),
                user=user,
            )

    def transfer_stock(self, quantity, target_inventory_item, user=None):
        if self.quantity < quantity:
            raise ValidationError("Cannot transfer more stock than available.")
        self.remove_stock(quantity, user)
        target_inventory_item.add_stock(quantity, user)
        StockMovement.objects.create(
            inventory_item=self,
            movement_type="transfer",
            location=self.administrative_unit.location_set.filter(type="warehouse").first(),
            quantity=quantity,
            date=now().date(),
            user=user,
        )

class ReceptionBatch(models.Model):
    receiving_date = models.DateField()
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE
    )  # Changed to CASCADE
    total_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    receiptID = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.supplier} - {self.receiving_date}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(default="")
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    tax_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    administrative_unit = models.ForeignKey(
        AdministrativeUnit, on_delete=models.CASCADE, default=1
    )
    type = models.CharField(
        max_length=50,
        choices=[("warehouse", "Warehouse"), ("storefront", "Storefront")],
        default="warehouse",
    )

    def __str__(self):
        return f"{str(self.id)} - {self.administrative_unit.name} - {self.type}"


class StockMovement(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    movement_type = models.CharField(
        max_length=50, choices=[("in", "In"), ("out", "Out"), ("transfer", "Transfer")]
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()
    date = models.DateField(default=now)  # Use callable `now` for default value
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   

    def __str__(self):
        return (
            f"{self.inventory_item.product.name} - {self.movement_type} - {self.date}"
        )
