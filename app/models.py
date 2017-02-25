# from django.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point

# Create your models here.

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.auth.models import AbstractUser


# class Place(models.Model):
#
#     class Meta:
#         verbose_name = "place"
#         verbose_name_plural = "places"
#
#     placename = models.CharField(
#         verbose_name="place name",
#         max_length=50,
#         blank=True
#     )
#     location = models.PointField(
#         verbose_name="location",
#         blank=True,
#         null=True
#     )
#     created = models.DateTimeField(
#         auto_now_add=True
#     )
#     modified = models.DateTimeField(
#         auto_now=True
#     )
#
#     objects = models.GeoManager()
#
#     def __str__(self):
#         return "{}, ({}), cr={}, mod={}".format(self.placename, self.location, self.created, self.modified)


class User(AbstractUser):
    last_location = models.PointField(
        verbose_name="last known location",
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.Manager()

    def __str__(self):
        return "{}, ({}), last seen at {} ... cr={}, mod={}".format(self.username, self.get_full_name(), self.last_location, self.created, self.modified)


class FriendGroup(models.Model):

    class Meta:
        verbose_name = "firends list"
        verbose_name_plural = "friends lists"

    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="name"
    )
    owner = models.ForeignKey(
        User,
        related_name="list_owner",
        verbose_name="owner",
        on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        User,
        through='UserFriendGroup'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.Manager()

    def __str__(self):
        return "{} owned by {}".format(self.name, self.owner)


class UserFriendGroup(models.Model):

    class Meta:
        unique_together = ['member', 'friend_group']
        verbose_name = "friend group members"
        verbose_name_plural = "friend group members"

    member = models.ForeignKey(
        User,
        verbose_name="member",
        on_delete=models.CASCADE
    )
    friend_group = models.ForeignKey(
        FriendGroup,
        verbose_name="friend group",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    # objects = models.Manager()

    def __str__(self):
        return "{} is a member of {}".format(self.member, self.friend_group)
