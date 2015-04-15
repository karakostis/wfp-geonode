from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from taggit.models import Tag

from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from geonode.api.api import TagResource, RegionResource, ProfileResource
from geonode.documents.models import Document
from geonode.base.models import Region

from models import WFPDocument, Category

class TagResourceSimple(TagResource):
    """ Tag API for models not inhereting form ResourceBase"""

    def dehydrate_count(self, bundle):
        tags = bundle.obj.taggit_taggeditem_items
        ctype = ContentType.objects.get_for_model(WFPDocument)
        count = tags.filter(
                content_type=ctype).count()
        return count

class WFPDocumentModelResource(ModelResource):
    """Base resource for gis application."""
    
    class Meta:
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()

class CategoryResource(WFPDocumentModelResource):
    """Resource  for Category model."""
    
    count = fields.IntegerField()
    
    def dehydrate_count(self, bundle):
        return bundle.obj.wfpdocument_set.count()
    
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'wfpcategories'
        excludes = ['id',]
        filtering = {
            'name': ALL,
        }
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()


class WFPDocumentResource(WFPDocumentModelResource):
    
    """Static Map API"""
    
    #document = fields.ToOneField(DocumentResource, 'document', full=True)
    keywords = fields.ToManyField(TagResource, 'keywords', null=True)
    categories = fields.ToManyField(CategoryResource, 'categories', full=True)
    regions = fields.ToManyField(RegionResource, 'regions', full=True)
    file_size = fields.CharField(attribute='get_file_size', readonly=True)
    owner = fields.ToOneField(ProfileResource, 'owner', full=True)
    
    
    #def build_filters(self, filters={}):
    #    orm_filters = super(WFPDocumentResource, self).build_filters(filters)
    #    categories = filters.getlist("categories__slug__in")
    #    regions = filters.getlist("regions__name__in")
    #    
    #    if categories:
    #        orm_filters.update({'categories__slug__in': categories})
    #    if regions:
    #        orm_filters.update({'regions__name__in': regions})
    #    return orm_filters

    #def apply_filters(self, request, applicable_filters):
    #    categories = applicable_filters.pop('categories__slug__in', None)
    #    regions = applicable_filters.pop('regions__name__in', None)

    #   wfpdocs = super(WFPDocumentResource, self).apply_filters(request, applicable_filters)
    #   filters = {}
    #   
    #   if categories:
    #       wfpdocs = wfpdocs.filter(categories__slug__in=categories).distinct()
    #   if regions:
    #       wfpdocs = wfpdocs.filter(regions__name__in=regions).distinct()
    #   return wfpdocs

    class Meta(CommonMetaApi):
        queryset = WFPDocument.objects.all().order_by('-date')
        resource_name = 'staticmaps'
        #filtering = {
            #'document': ALL_WITH_RELATIONS,
        #    'categories': ALL_WITH_RELATIONS,
        #    'date_updated': ALL,
        #}
        #include_resource_uri = True
        #allowed_methods = ['get']
        #authentication = BasicAuthentication()
        filtering = {
            'keywords': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
            'regions': ALL_WITH_RELATIONS,
            'date': ALL,
        }
        excludes = [
          'csw_anytext', 'metadata_xml'
          'owner__email',
        ]
        
    def dehydrate_page_format(self, bundle):
        return WFPDocument.FORMAT_CHOICES[bundle.data['page_format']][1]
        
    def dehydrate_orientation(self, bundle):
        return WFPDocument.ORIENTATION_CHOICES[bundle.data['orientation']][1]
        
    def build_schema(self):
        base_schema = super(WFPDocumentResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema
        

