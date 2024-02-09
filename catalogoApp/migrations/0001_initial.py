# Generated by Django 5.0.2 on 2024-02-08 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.TextField()),
                ('comuna', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=200)),
                ('cantidadPedidos', models.IntegerField()),
                ('deuda', models.BooleanField()),
                ('extra', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to='imagenes')),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProducto', models.CharField(max_length=200)),
                ('identificador', models.CharField(max_length=200)),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('resumenPedido', models.TextField()),
                ('estado_entrega', models.BooleanField(default=False)),
                ('estado_pago', models.BooleanField(default=False)),
                ('hora', models.CharField(max_length=200)),
                ('dia', models.CharField(max_length=200)),
                ('extra', models.CharField(max_length=200)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogoApp.clientes')),
            ],
        ),
    ]
