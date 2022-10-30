from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Legend(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class Planeswalker(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class Land(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class GreenSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class BlueSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class BlackSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class WhiteSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class RedSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class ColorlessSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class MulticolorSpells(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)

class Bulk(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1)
    extra = models.CharField(max_length=6,default="NONE")
    set = models.CharField(max_length=5)
    collector_number = models.IntegerField()
    old_price = models.DecimalField(decimal_places=2,max_digits=6)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    price_quantity = models.DecimalField(decimal_places=2,max_digits=6)
