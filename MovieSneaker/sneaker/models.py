from django.db import models
from django import forms 
from django.forms import ModelForm

class ZipCode(models.Model):
    zipcode = models.CharField(max_length=100, blank=False)

class ZipCodeForm(ModelForm):
    class Meta:
        model = ZipCode

class Movie(models.Model):
    name = models.CharField(max_length=256, blank=False)
    runtime = models.IntegerField(blank=False) # in minutes
    description = models.CharField(max_length=512, blank=True)
    notes = models.CharField(max_length=1024, blank=True)

class Showing(models.Model):
    movie = models.ForeignKey(Movie)
    venue = models.ForeignKey(Venue)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)

class Venue(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=512)
    # This isn't the actual zipcode this venue is in
    # Just the set of zipcodes this is considered close to
    zipcode = models.ManyToManyField(ZipCode)
    description = models.CharField(max_length=1024,blank=True)

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
