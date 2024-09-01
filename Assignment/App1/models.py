from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Leads(models.Model):
    lead_name = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    product = models.ManyToManyField(Product, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    