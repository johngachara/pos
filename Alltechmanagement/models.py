from django.db import models

# Create your models here.
class Shop_stock(models.Model):
    product_name = models.CharField(max_length=30,unique=True)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=7)
    def __str__(self):
        return self.product_name
