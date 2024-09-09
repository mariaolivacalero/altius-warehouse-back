from django.db import models
from custom_auth.models import User
from django.db import IntegrityError
from django.utils.timezone import now
from django.core.exceptions import ValidationError

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
    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    warehouse_quantity = models.PositiveIntegerField()
    storefront_quantity = models.PositiveIntegerField()
    administrative_unit = models.ForeignKey(
        AdministrativeUnit, on_delete=models.SET_NULL, null=True
    )
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.batch.party} - {self.batch.receiving_date}"

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            warehouse_location = Location.objects.filter(
                administrative_unit=self.administrative_unit, type="warehouse"
            ).first()

            if warehouse_location:
                Reception.objects.create(
                    inventory_item=self,
                    batch=self.batch,
                    location=warehouse_location,
                    quantity=self.quantity,
                    date=now().date(),
                    user=user,
                )

    def add_stock(self, quantity, user=None):
        self.quantity += quantity
        self.warehouse_quantity += quantity
        self.save()
        warehouse_location = Location.objects.filter(
            administrative_unit=self.administrative_unit, type="warehouse"
        ).first()
        if warehouse_location:
            Reception.objects.create(
                inventory_item=self,
                batch=self.batch,
                location=warehouse_location,
                quantity=quantity,
                date=now().date(),
                user=user,
            )

    def remove_stock(self, quantity, user=None):
        if self.quantity < quantity:
            raise ValidationError("Cannot remove more stock than available.")
        self.quantity -= quantity
        self.warehouse_quantity -= quantity
        self.save()
        warehouse_location = Location.objects.filter(
            administrative_unit=self.administrative_unit, type="warehouse"
        ).first()
        if warehouse_location:
            Dispatch.objects.create(
                inventory_item=self,
                batch=self.batch,
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
        from_location = self.administrative_unit.location_set.filter(type="warehouse").first()
        to_location = target_inventory_item.administrative_unit.location_set.filter(type="warehouse").first()
        if from_location and to_location:
            StoreStocking.objects.create(
                inventory_item=self,
                from_location=from_location,
                to_location=to_location,
                location=to_location,
                quantity=quantity,
                date=now().date(),
                user=user,
            )

class Batch(models.Model):  # Renamed from ReceptionBatch
    receiving_date = models.DateField()
    party = models.ForeignKey(
        "Party", on_delete=models.CASCADE
    )  # Changed from supplier
    total_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    receiptID = models.CharField(max_length=50, unique=True)
    type = models.CharField(
        max_length=10, choices=[("reception", "Reception"), ("dispatch", "Dispatch")]
    )

    def __str__(self):
        return f"{self.party} - {self.receiving_date} - {self.type}"


class Party(models.Model):  # Renamed from Supplier
    name = models.CharField(max_length=255)
    address = models.TextField(default="")
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    tax_id = models.CharField(max_length=50)
    type = models.CharField(
        max_length=10, choices=[("supplier", "Supplier"), ("receiver", "Receiver")]
    )

    def __str__(self):
        return f"{self.name} - {self.type}"


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


class BaseStockOperation(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Reception(BaseStockOperation):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reception: {self.inventory_item.product.name} - {self.quantity} - {self.date}"


class Dispatch(BaseStockOperation):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dispatch: {self.inventory_item.product.name} - {self.quantity} - {self.date}"


class StoreStocking(BaseStockOperation):
    from_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="stocking_from"
    )
    to_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="stocking_to"
    )

    def __str__(self):
        return f"Store Stocking: {self.inventory_item.product.name} - {self.quantity} - {self.date}"


class PickUp(BaseStockOperation):
    beneficiary = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pickups"
    )

    def __str__(self):
        return f"Pick Up: {self.inventory_item.product.name} - {self.quantity} - {self.date}"
