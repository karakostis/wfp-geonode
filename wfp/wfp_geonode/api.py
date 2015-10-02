from django.contrib.auth import get_user_model

from tastypie import fields
from tastypie.constants import ALL
from guardian.shortcuts import get_objects_for_user

from geonode.api.api import ProfileResource
from geonode.api.api import CountJSONSerializer

from wfp.wfpdocs.models import WFPDocument


class WfpProfileResource(ProfileResource):
    """ WFP Profile api """

    wfpdocs_count = fields.IntegerField(default=0)

    def dehydrate_wfpdocs_count(self, bundle):
        obj_with_perms = get_objects_for_user(bundle.request.user,
                                              'base.view_resourcebase').instance_of(WFPDocument)
        return bundle.obj.resourcebase_set.filter(id__in=obj_with_perms.values('id')).distinct().count()

    class Meta:
        queryset = get_user_model().objects.exclude(username='AnonymousUser')
        resource_name = 'wfp-profiles'
        allowed_methods = ['get']
        ordering = ['username', 'date_joined']
        excludes = ['is_staff', 'password', 'is_superuser',
                    'is_active', 'last_login']

        filtering = {
            'username': ALL,
        }
        serializer = CountJSONSerializer()
