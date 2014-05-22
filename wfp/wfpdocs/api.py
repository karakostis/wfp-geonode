from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from geonode.documents.models import Document
from geonode.base.models import Region
from geonode.security.models import GenericObjectRoleMapping

from models import WFPDocument, Category

class WFPDocumentModelResource(ModelResource):
    """Base resource for gis application."""
    
    class Meta:
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()
    
class CategoryResource(WFPDocumentModelResource):
    """Resource  for Category model."""
    
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        excludes = ['id',]
        filtering = {
            'name': ALL_WITH_RELATIONS,
        }
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        
class RegionResource(WFPDocumentModelResource):
    """Resource  for Region model."""
    
    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        excludes = ['id',]
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        
class DocumentResource(WFPDocumentModelResource):
    """Resource  for Document model."""
    regions = fields.ToManyField(RegionResource, 'regions', full=True)
    geonode_page = fields.CharField(attribute='get_absolute_url', readonly=True)
    geonode_file = fields.FileField(attribute='doc_file')
    thumbnail = fields.CharField(attribute='get_thumbnail_url', readonly=True)
    is_public = fields.BooleanField(default=True)
    
    class Meta:
        queryset = Document.objects.all()

        resource_name = 'document'
        fields = ['title', 'date', 'thumbnail',]
        filtering = {
            'title': ALL,
            'date': ALL_WITH_RELATIONS,
        }
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        
    def dehydrate_is_public(self, bundle):
        # TODO find a better way to avoid this additional query for every resource
        private_docs = GenericObjectRoleMapping.objects.filter(subject=u'anonymous', object_ct__name='document').values_list('object_id', flat=True)
        public = self.instance.id in private_docs
        return public
        
class WFPDocumentResource(WFPDocumentModelResource):
    """Resource  for WFPDocument model."""
    document = fields.ToOneField(DocumentResource, 'document', full=True)
    categories = fields.ToManyField(CategoryResource, 'categories', full=True)
    file_size = fields.CharField(attribute='get_file_size', readonly=True)
    
    class Meta:
        queryset = WFPDocument.objects.all()
        resource_name = 'wfp-document'
        filtering = {
            'document': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
            'date_updated': ALL,
        }
        include_resource_uri = True
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        
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
        

