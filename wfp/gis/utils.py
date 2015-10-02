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

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from geonode.people.models import Profile
from models import Office, Employee


def import_offices():
    Office.objects.all().delete()
    ds = DataSource('wfp/gis/data/wld_poi_facilities_wfp.shp')
    print(ds)
    lyr = ds[0]
    print lyr.fields
    # 'wfpid', u'place', u'facility', u'status', u'iso3', u'iso3_op', u'country'
    # u'locprecisi', u'latitude', u'longitude', u'wfpregion', u'nat_staff',
    # u'int_staff', u'lastcheckd', u'remarks', u'source', u'createdate',
    # u'updatedate', u'objectidol', u'precisiono', u'verifiedol'
    for feat in lyr:
        geom = feat.geom
        pnt = GEOSGeometry(geom.ewkt)
        wfpid = feat.get('wfpid')
        place = feat.get('place')
        facility = feat.get('facility')
        status = feat.get('status')
        country = feat.get('country')
        wfpregion = feat.get('wfpregion')
        lastcheckd = feat.get('lastcheckd')
        createdate = feat.get('createdate')
        updatedate = feat.get('updatedate')
        source = feat.get('source')
        office = Office(
            geometry=pnt, wfpid=wfpid, place=place, facility=facility,
            wfpregion=wfpregion, lastcheckd=lastcheckd, source=source,
            status=status, country=country, createdate=createdate,
            updatedate=updatedate
        )
        office.save()


def create_employees():
    Employee.objects.all().delete()
    o = Office.objects.all()[0]
    for p in Profile.objects.all():
        e = Employee(profile=p, office=o)
        e.save()
