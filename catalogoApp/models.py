from django.db import models

# Create your models here.

class Users(models.Model):
    userName = models.CharField(max_length=200) # Unique
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.userName
    
class Clientes(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    comuna = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200) # Unique
    cantidadPedidos = models.IntegerField()
    deuda = models.BooleanField()
    extra = models.TextField(null=True)

    def __str__(self):
        return self.telefono
    
class Productos(models.Model):
    nombreProducto = models.CharField(max_length=200)
    identificador = models.CharField(max_length=200) # Unique
    stock = models.IntegerField()

    def __str__(self):
        return self.identificador
    
class Pedidos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    precio = models.IntegerField()
    resumenPedido = models.TextField()
    estado_entrega = models.BooleanField(default=False)
    estado_pago = models.BooleanField(default=False)
    hora = models.CharField(max_length=200)
    dia = models.CharField(max_length=200)
    extra = models.CharField(max_length=200)

class Imagenes(models.Model):
    imagen = models.ImageField(upload_to="imagenes",null=True)