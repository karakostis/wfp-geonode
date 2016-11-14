#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.gis.db import models as gismodels

from geonode.people.models import Profile


class Office(gismodels.Model):
    """
    Model for WFP Office.
    """
    wfpid = gismodels.IntegerField(null=True, blank=True)
    place = gismodels.CharField(max_length=254)
    facility = gismodels.CharField(max_length=254, null=True, blank=True)
    status = gismodels.CharField(max_length=254, null=True, blank=True)
    iso3 = gismodels.CharField(max_length=254, null=True, blank=True)
    iso3_op = gismodels.CharField(max_length=254, null=True, blank=True)
    country = gismodels.CharField(max_length=254, null=True, blank=True)
    locprecisi = gismodels.CharField(max_length=254, null=True, blank=True)
    latitude = gismodels.FloatField(null=True, blank=True)
    longitude = gismodels.FloatField(null=True, blank=True)
    wfpregion = gismodels.CharField(max_length=254, null=True, blank=True)
    nat_staff = gismodels.IntegerField(null=True, blank=True)
    int_staff = gismodels.IntegerField(null=True, blank=True)
    lastcheckd = gismodels.DateField(null=True, blank=True)
    remarks = gismodels.CharField(max_length=254, null=True, blank=True)
    source = gismodels.CharField(max_length=254, null=True, blank=True)
    createdate = gismodels.DateField(null=True, blank=True)
    updatedate = gismodels.DateField(null=True, blank=True)
    objectidol = gismodels.FloatField(null=True, blank=True)
    precisiono = gismodels.CharField(max_length=254, null=True, blank=True)
    verifiedol = gismodels.CharField(max_length=254, null=True, blank=True)
    geometry = gismodels.PointField()
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.place)

    class Meta:
        ordering = ['place']


class Employee(models.Model):
    """
    Model for WFP Profile.
    """

    GIS_LEVEL_CHOICES = (
        (0, 'Basic'),
        (1, 'Intermediate'),
        (2, 'Advanced'),
    )

    DUTIES_CHOICES = (
        (0, 'GIS'),
        (1, 'Not GIS')
    )

    gis_level = models.IntegerField(null=True, blank=True, choices=GIS_LEVEL_CHOICES)
    duties_type = models.IntegerField(blank=True, null=True, choices=DUTIES_CHOICES)
    profile = models.OneToOneField(Profile, primary_key=True)
    office = models.ForeignKey(Office, null=True, blank=True)

    @property
    def geometry(self):
        return self.office.geometry

    @property
    def place(self):
        return self.office.place

    @property
    def country(self):
        return self.office.country

    @property
    def wfpregion(self):
        return self.office.wfpregion

    @property
    def facility(self):
        return self.office.facility

    @property
    def name(self):
        return self.profile.name

    @property
    def position(self):
        return self.profile.position

    def __unicode__(self):
        if self.office:
            return '%s in %s' % (self.profile.get_full_name(), self.office.place)

class CustomThumbnail(models.Model):
    """
    Model for custom thumbnails for WFP GeoNode objects
    """
    thumbnail = models.ImageField(upload_to='custom_thumbs')
    title = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.title
