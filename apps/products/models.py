# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class ProductManager(models.Manager):
    pass

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="created_products")
    users = models.ManyToManyField(User, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

def __str__(self):
    output = "<Product object: {}>".format(self.product_name)
    return output
