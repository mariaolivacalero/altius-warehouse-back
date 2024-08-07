# Generated by Django 4.2.14 on 2024-08-07 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_category_location_remove_supplier_contact_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receptionbatch',
            name='status',
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='reception_batch',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='inventory.receptionbatch'),
            preserve_default=False,
        ),
    ]