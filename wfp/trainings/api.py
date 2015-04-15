from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from taggit.models import Tag

from geonode.api.resourcebase_api import CommonModelApi, LayerResource
from geonode.api.api import TagResource

from .models import Training


class TagResourceSimple(TagResource):
    """ Tag API for models not inhereting form ResourceBase"""
    
    def dehydrate_count(self, bundle):
        tags = bundle.obj.taggit_taggeditem_items
        ctype = ContentType.objects.get_for_model(Training)
        count = tags.filter(
                content_type=ctype).count()
        return count
    
class TrainingResource(ModelResource):

    """ Training API """

    keywords = fields.ToManyField(TagResourceSimple, 'keywords', null=True, full=True)
    layers = fields.ToManyField(LayerResource, 'layers', null=True, full=True)
    
    def build_filters(self, filters={}):
        orm_filters = super(TrainingResource, self).build_filters(filters)
        keywords = filters.getlist("keywords__slug__in")
        
        if keywords:
            #for keyword in keywords:
                #orm_filters.update({'keywords__slug__in': filters['keywords__slug__in']})
            orm_filters.update({'keywords__slug__in': keywords})
        #import ipdb;ipdb.set_trace()
        print orm_filters
        return orm_filters
        
    def apply_filters(self, request, applicable_filters):
        keywords = applicable_filters.pop('keywords__slug__in', None)
        trainings = super(TrainingResource, self).apply_filters(request, applicable_filters)
        filters = {}
        #import ipdb;ipdb.set_trace()
        if keywords:
            #filters.update(dict(keywords__slug__in=[keywords]))
            #base_object_list.filter(keywords).distinct()
            trainings = trainings.filter(keywords__slug__in=keywords).distinct()
        return trainings
        
    class Meta:
        queryset = Training.objects.all().order_by('title')
        resource_name = 'trainings'
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'keywords': ALL_WITH_RELATIONS,
            'layers': ALL_WITH_RELATIONS,
        }
        include_absolute_url = True
