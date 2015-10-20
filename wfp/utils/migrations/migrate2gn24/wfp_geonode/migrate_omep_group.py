#!/usr/bin/python
import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings.default")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from geonode.people.models import Profile
from geonode.groups.models import GroupProfile

#OMEP-GIS-Team

print 'Creating the OMEP-GIS-Team group...'
gp = GroupProfile.objects.create(
    title='OMEP GIS Team',
    slug='omep-gis-team',
    description='Group containg all of the OMEP GIS Team contacts for GeoNode',
    access='public',
)

users = (
            'paolo.corti',
            'francesco.stompanato',
            'filippo.pongelli',
            'andrea.amparore',
            'rashid.kashif',
            'lara.prades',
            'mattia.pinzone',
            'paola.difrancesco',
            'thierry.crevoisier',
        )

for username in users:
    profile = Profile.objects.get(username=username)
    print 'Adding %s to the group' % profile.username
    gp.join(profile)


