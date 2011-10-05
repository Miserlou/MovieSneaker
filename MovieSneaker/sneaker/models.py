from django.db import models
from django import forms 
from django.forms import ModelForm

class ZipCode(models.Model):
    zipcode = models.CharField(max_length=100, blank=False)

class ZipCodeForm(ModelForm):
    class Meta:
        model = ZipCode 
