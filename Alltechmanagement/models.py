from django.db import models

# Create your models here.
class Shop_stock(models.Model):
    product_name = models.CharField(max_length=30,unique=True)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=7)
    def __str__(self):
        return self.product_name


class Home_stock(models.Model):
    product_name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField()
    def __str__(self):
        return self.product_name


class Saved_transactions(models.Model):
    product_name = models.CharField(max_length=20)
    selling_price = models.DecimalField(max_digits=7,decimal_places=2)
    quantity = models.IntegerField()
    def __str__(self):
        return self.product_name

class Completed_transactions(models.Model):
    product_name = models.CharField(max_length=20)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_name
