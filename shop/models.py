from IPython.core.magic_arguments import defaults

from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50,default="")
    dec = models.CharField(max_length=300,default="")
    pu_date = models.DateField( )
    price =models.IntegerField(default=0)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    image = models.ImageField(upload_to="shop/images")
    product_id = models.IntegerField(default=0)
    def __str__(self):
        return self .product_name
 # myprod = Product(product_name="mouse",category="computer",subcategory="devices",price=12,dec="chooha hai",pu_date=timezone.now())



class Orders(models.Model):
    order_id = models.AutoField(primary_key = True,default=0)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=411)
    city= models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default=0)
    def __str__(self):
        return f"Order #{self.order_id} - {self.name}"

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key = True,default=0)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length = 5000)
    timestamp = models.DateField(default=timezone.now)
    def __str__(self):
        return self.update_desc[0:7] + "...."

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name