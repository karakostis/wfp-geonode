from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.conf import settings

from guardian.shortcuts import get_objects_for_user
from guardian.shortcuts import get_anonymous_user

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
    title = "WFP GeoNode Maps Repository RSS"
    link = settings.SITEURL
    description = "Latest maps from WFP/GeoNode Maps Repository."

    def items(self):
        anonymous_user = get_anonymous_user()
        public_wfpdocs_ids = get_objects_for_user(
                anonymous_user, 'base.view_resourcebase'
            ).instance_of(WFPDocument).values_list('id', flat=True)
        public_wfpdocs = WFPDocument.objects.filter(id__in=public_wfpdocs_ids)
        return public_wfpdocs.order_by('-date')[:20]

    # Elements for each item

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date

    def item_author_name(self, item):
        return 'WFP GeoNode'

    def item_author_email(self, item):
        return settings.THEME_ACCOUNT_CONTACT_EMAIL

    def item_extra_kwargs(self, obj):
        return {
            'category': obj.get_categories(),
            'epweb:thumbURL': obj.get_thumbnail_url(),
            'epweb:previewURL': obj.get_thumbnail_url(),
            'epweb:source': obj.source,
            'epweb:createDate': str(obj.date),
            'epweb:fileType': obj.extension.upper(),
            'epweb:fileSize': str(obj.get_file_size()),
            'epweb:printSize': WFPDocument.FORMAT_CHOICES[obj.page_format][1],
            'epweb:countries': obj.regions.all(),
        }
