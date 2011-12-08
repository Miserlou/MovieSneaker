from django.db import models
from django import forms 
from django.forms import ModelForm

class ZipCode(models.Model):
    zipcode = models.CharField(max_length=100, blank=False)

class ZipCodeForm(ModelForm):
    class Meta:
        model = ZipCode 

design_comment = """
- Movie
  - name :: VARCHAR(256) // Movie Name (Year) guarantees unique, we'll figure something out if there's an exception
  - runtime (seconds) :: INTEGER
  - description :: VARCHAR(1024)
  - notes :: VARCHAR(512)

- Showing
  - movie :: ForeignKey(Movie)
  - venue :: ForeignKey(Venue)
  - start :: DATETIME
  - end :: DATETIME

- Venue
  - id
  - name :: VARCHAR(256)
  - address :: VARCHAR(512)
  - zipcode :: CHAR(5)
  - description :: VARCHAR(1024)
"""
