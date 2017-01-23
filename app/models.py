from django.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point

# Create your models here.

from django.contrib.gis.db import models
from django.contrib.gis import geos

class Place(models.Model):

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"

    placename = models.CharField(
        verbose_name="place name",
        max_length=50,
        blank=True
    )
    location = models.PointField(
        verbose_name="location",
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    objects = models.GeoManager()

    def __str__(self):
        return "{}, ({}), cr={}, mod={}".format(self.placename, self.location, self.created, self.modified)

