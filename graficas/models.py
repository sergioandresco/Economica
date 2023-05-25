from django.db import models

class Producto(models.Model):
    producto = models.CharField(max_length=100)
    ano = models.IntegerField(default=2023)
    mes = models.CharField(max_length=20, default="enero")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=10, default=1)

    def __str__(self):
        return self.producto
