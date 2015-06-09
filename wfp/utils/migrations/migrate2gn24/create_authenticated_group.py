import os, sys

path = os.path.dirname(__file__)
geonode_path = os.path.abspath(os.path.join(path, '../../../..'))
sys.path.append(geonode_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfp.settings._geonode24")

from geonode.groups.models import GroupProfile
from geonode.people.models import Profile

print 'Creating the authenticated group.'
gp = GroupProfile.objects.create(
    title='Authenticated GeoNode Users',
    slug='authenticated',
    description='Group containg all of the registered GeoNode users',
    access='public',
)
# assign all existing users to this group
print 'Now adding all users to the group:'
for profile in Profile.objects.all():
    if profile.username != 'AnonymousUser':
        print 'Adding %s to the group' % profile.username
        gp.join(profile)
