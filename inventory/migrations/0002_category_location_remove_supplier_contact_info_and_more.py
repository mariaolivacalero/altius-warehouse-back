# Generated by Django 4.2.14 on 2024-08-07 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='contact_info',
        ),
        migrations.AddField(
            model_name='receptionbatch',
            name='status',
            field=models.CharField(choices=[('received', 'Received'), ('in_process', 'In Process'), ('completed', 'Completed')], default='received', max_length=20),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='reception_batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.receptionbatch'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='supplier',
            name='contact_person',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receptionbatch',
            name='supplier',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='movement_type',
            field=models.CharField(choices=[('in', 'In'), ('out', 'Out'), ('transfer', 'Transfer')], max_length=50),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.location'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.category'),
        ),
    ]