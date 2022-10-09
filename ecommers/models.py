from asyncio.windows_events import NULL
from email.policy import default
from http.client import PAYMENT_REQUIRED
from operator import mod
from statistics import mode
from django.db import models
import datetime
from django.utils import timezone
import os
from uuid import uuid4

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    email=models.EmailField(max_length=20)
    code=models.IntegerField(default=0)
    verify=models.IntegerField()

CATEGORY_CHOICES = (
    ('Men','men'),
    ('Women','women'),
    ('Electronics','electronics'),
)
def path_and_rename(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Products(models.Model):
    products_name=models.CharField(max_length=50)
    products_desc=models.TextField()
    products_price=models.IntegerField()
    products_qty=models.IntegerField()
    products_Image=models.ImageField(upload_to=path_and_rename)
    products_category=models.CharField(max_length=50,choices=CATEGORY_CHOICES,default='men')

class Add_to_cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField()

class user_dateils(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    addresss=models.TextField()
    phone=models.IntegerField()
    first_name=models.CharField(max_length=25,default=NULL)
    email=models.EmailField(max_length=50,default=NULL)
    last_name=models.CharField(max_length=25,default=NULL)

class coupon_code(models.Model):
    coupon_name=models.CharField(max_length=15)
    coupon_price=models.IntegerField()

class placed_order(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField()
    coupon_amount=models.IntegerField()
    payment_request_id=models.CharField(max_length=300,default=NULL)
    payment_id=models.IntegerField()
    

class wishlist_item(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Products,on_delete=models.CASCADE)