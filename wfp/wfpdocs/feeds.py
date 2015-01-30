from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from django.conf import settings

from models import WFPDocument

class CustomFeedGenerator(Rss201rev2Feed):
    """
    Custom feed generator, for including epweb custom elements.
    """
    def root_attributes(self):
        attrs = super(CustomFeedGenerator, self).root_attributes()
        attrs['xmlns:epweb'] = 'http://geonode.wfp.org/'
        return attrs
        
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'category', item['category'])
        handler.addQuickElement(u'epweb:thumbURL', item['epweb:thumbURL'])
        handler.addQuickElement(u'epweb:previewURL', item['epweb:previewURL'])
        handler.addQuickElement(u'epweb:source', item['epweb:source'])
        handler.addQuickElement(u'epweb:createDate', item['epweb:createDate'])
        handler.addQuickElement(u'epweb:fileType', item['epweb:fileType'])
        handler.addQuickElement(u'epweb:fileSize', item['epweb:fileSize'])
        handler.addQuickElement(u'epweb:printSize', item['epweb:printSize'])
        handler.startElement(u'epweb:countries', {})
        for region in item['epweb:countries']:
            handler.addQuickElement(u'epweb:country', region.name, {
                'iso3': region.code,
            })
        handler.endElement(u'epweb:countries')

        
class WFPDocumentsFeed(Feed):
    """
    RSS feed of all public static maps.
    """
    
    # Elements for the top-level, channel
    
    feed_type = CustomFeedGenerator
    title = "WFP/OMEP Maps Repository RSS"
    link = settings.SITEURL
    description = "Latest maps from WFP/GeoNode Maps Repository."

    def items(self):
        from geonode.security.models import GenericObjectRoleMapping
        public_docs = GenericObjectRoleMapping.objects.filter(subject=u'anonymous', object_ct__name='document').values_list('object_id', flat=True)
        public_wfpdocs = WFPDocument.objects.filter(document__id__in=public_docs)
        return public_wfpdocs.order_by('-document__date')[:20]

    # Elements for each item
    
    def item_title(self, item):
        return item.document.title

    def item_description(self, item):
        return item.document.title
    
    def item_pubdate(self, item):
        return item.document.date
        
    def item_author_name(self, item):
        return 'OMEP GIS'
            
    def item_author_email(self, item):
        return 'omep.gis@wfp.org'
    
    def item_extra_kwargs(self, obj):
        thumb_url = '%s%s' % (settings.SITEURL[:-1], 
            obj.document.get_thumbnail_url())
        return {
            'category': obj.get_categories(),
            'epweb:thumbURL' : thumb_url,
            'epweb:previewURL' : thumb_url,
            'epweb:source' : obj.source,
            'epweb:createDate' : str(obj.document.date),
            'epweb:fileType' : obj.document.extension.upper(),
            'epweb:fileSize' : str(obj.get_file_size()),
            'epweb:printSize' : WFPDocument.FORMAT_CHOICES[obj.page_format][1],
            'epweb:countries' : obj.document.regions.all(),
        }

