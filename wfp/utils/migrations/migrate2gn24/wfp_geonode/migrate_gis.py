#!/usr/bin/python
import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings.default")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import utils
from geonode.people.models import Profile
from wfp.gis.models import Office, Employee

src = utils.get_src()
src_cur = src.cursor()

# 1. first, migrate offices
sql_offices_fields = """
    wfpid,
    place,
    facility,
    status,
    iso3,
    iso3_op,
    country,
    locprecisi,
    latitude,
    longitude,
    wfpregion,
    nat_staff,
    int_staff,
    lastcheckd,
    remarks,
    source,
    createdate,
    updatedate,
    objectidol,
    precisiono,
    verifiedol,
    geometry
"""

sql_offices = "SELECT %s FROM gis_office" % sql_offices_fields
src_cur.execute(sql_offices)

Office.objects.all().delete()
for src_row in src_cur:
    print 'New office for %s added' % src_row[1]
    office = Office(
        wfpid = src_row[0],
        place = src_row[1],
        facility = src_row[2],
        status = src_row[3],
        iso3 = src_row[4],
        iso3_op = src_row[5],
        country = src_row[6],
        locprecisi = src_row[7],
        latitude = src_row[8],
        longitude = src_row[9],
        wfpregion = src_row[10],
        nat_staff = src_row[11],
        int_staff = src_row[12],
        lastcheckd = src_row[13],
        remarks = src_row[14],
        source = src_row[15],
        createdate = src_row[16],
        updatedate = src_row[17],
        objectidol = src_row[18],
        precisiono = src_row[19],
        verifiedol = src_row[20],
        geometry = src_row[21]
    )
    office.save()

# 2. second, migrate empoyees
sql_employees = """
    SELECT gis_level, duties_type, username, wfpid FROM 
    (
	    SELECT gis_level, duties_type, user_id, wfpid
	    FROM gis_employee AS e
	    JOIN gis_office AS o
	    ON e.office_id = o.id
	    JOIN people_profile AS p
	    ON e.profile_id = p.id
    ) AS e
    JOIN auth_user AS u
    ON e.user_id = u.id
"""
src_cur.execute(sql_employees)

Employee.objects.all().delete()
for src_row in src_cur:
    print 'New employee for %s added' % src_row[2]
    office = Office.objects.get(wfpid = src_row[3])
    profile = Profile.objects.get(username = src_row[2])
    employee = Employee(
        gis_level = src_row[0],
        duties_type = src_row[1],
        profile = profile,
        office = office
    )
    employee.save()

src_cur.close()
src.close()
