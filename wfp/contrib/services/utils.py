import httplib2
import math
from geonode.base.models import Link
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from django.conf import settings
from urlparse import urljoin

http_client = httplib2.Http()

def forward_mercator(lonlat):
    """
        Given geographic coordinates, return a x,y tuple in spherical mercator.

        If the lat value is out of range, -inf will be returned as the y value
    """
    x = lonlat[0] * 20037508.34 / 180
    try:
        # With data sets that only have one point the value of this
        # expression becomes negative infinity. In order to continue,
        # we wrap this in a try catch block.
        n = math.tan((90 + lonlat[1]) * math.pi / 360)
    except ValueError:
        n = 0
    if n <= 0:
        y = float("-inf")
    else:
        y = math.log(n) / math.pi * 20037508.34
    return (x, y)


def inverse_mercator(xy):
    """
        Given coordinates in spherical mercator, return a lon,lat tuple.
    """
    lon = (xy[0] / 20037508.34) * 180
    lat = (xy[1] / 20037508.34) * 180
    lat = 180/math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return (lon, lat)
    
def set_attributes(layer, overwrite=False):
    """
    Retrieve layer attribute names & types from Geoserver,
    then store in GeoNode database using Attribute model
    """
    attribute_map = []
    if layer.storeType == "dataStore":
        dft_url = ogc_server_settings.LOCATION + "wfs?" + urllib.urlencode({
            "service": "wfs",
            "version": "1.0.0",
            "request": "DescribeFeatureType",
            "typename": layer.typename.encode('utf-8'),
            })
        # The code below will fail if http_client cannot be imported
        body = http_client.request(dft_url)[1]
        doc = etree.fromstring(body)
        path = ".//{xsd}extension/{xsd}sequence/{xsd}element".format(xsd="{http://www.w3.org/2001/XMLSchema}")

        attribute_map = [[n.attrib["name"], n.attrib["type"]] for n in doc.findall(path)
                         if n.attrib.get("name") and n.attrib.get("type")]

    elif layer.storeType == "coverageStore":
        dc_url = ogc_server_settings.LOCATION + "wcs?" + urllib.urlencode({
            "service": "wcs",
            "version": "1.1.0",
            "request": "DescribeCoverage",
            "identifiers": layer.typename.encode('utf-8')
        })
        try:
            response, body = http_client.request(dc_url)
            doc = etree.fromstring(body)
            path = ".//{wcs}Axis/{wcs}AvailableKeys/{wcs}Key".format(wcs="{http://www.opengis.net/wcs/1.1.1}")
            attribute_map = [[n.text,"raster"] for n in doc.findall(path)]
        except Exception:
            attribute_map = []

    attributes = layer.attribute_set.all()
    # Delete existing attributes if they no longer exist in an updated layer
    for la in attributes:
        lafound = False
        for field, ftype in attribute_map:
            if field == la.attribute:
                lafound = True
        if overwrite or not lafound:
            logger.debug("Going to delete [%s] for [%s]", la.attribute, layer.name.encode('utf-8'))
            la.delete()

    # Add new layer attributes if they don't already exist
    if attribute_map is not None:
        iter = len(Attribute.objects.filter(layer=layer)) + 1
        for field, ftype in attribute_map:
            if field is not None:
                la, created = Attribute.objects.get_or_create(layer=layer, attribute=field, attribute_type=ftype)
                if created:
                    if is_layer_attribute_aggregable(layer.storeType, field, ftype):
                        logger.debug("Generating layer attribute statistics")
                        result = get_attribute_statistics(layer.name, field)
                        if result is not None:
                            la.count = result['Count']
                            la.min = result['Min']
                            la.max = result['Max']
                            la.average = result['Average']
                            la.median = result['Median']
                            la.stddev = result['StandardDeviation']
                            la.sum = result['Sum']
                            la.unique_values = result['unique_values']
                            la.last_stats_updated = datetime.datetime.now()
                    la.attribute_label = field.title()
                    la.visible = ftype.find("gml:") != 0
                    la.display_order = iter
                    la.save()
                    iter += 1
                    logger.debug("Created [%s] attribute for [%s]", field, layer.name.encode('utf-8'))
    else:
        logger.debug("No attributes found")
        
def inverse_mercator(xy):
    """
        Given coordinates in spherical mercator, return a lon,lat tuple.
    """
    lon = (xy[0] / 20037508.34) * 180
    lat = (xy[1] / 20037508.34) * 180
    lat = 180/math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return (lon, lat)

def llbbox_to_mercator(llbbox):
    minlonlat = forward_mercator([llbbox[0],llbbox[1]])
    maxlonlat = forward_mercator([llbbox[2],llbbox[3]])
    return [minlonlat[0],minlonlat[1],maxlonlat[0],maxlonlat[1]]

def mercator_to_llbbox(bbox):
    minlonlat = inverse_mercator([bbox[0],bbox[1]])
    maxlonlat = inverse_mercator([bbox[2],bbox[3]])
    return [minlonlat[0],minlonlat[1],maxlonlat[0],maxlonlat[1]]

def create_thumbnail(instance, thumbnail_remote_url):
    BBOX_DIFFERENCE_THRESHOLD = 1e-5

    #Check if the bbox is invalid
    valid_x = (float(instance.bbox_x0) - float(instance.bbox_x1))**2 > BBOX_DIFFERENCE_THRESHOLD
    valid_y = (float(instance.bbox_y1) - float(instance.bbox_y0))**2 > BBOX_DIFFERENCE_THRESHOLD

    image = None

    if valid_x and valid_y:
        Link.objects.get_or_create(resource= instance.resourcebase_ptr,
                        url=thumbnail_remote_url,
                        defaults=dict(
                            extension='png',
                            name=_("Remote Thumbnail"),
                            mime='image/png',
                            link_type='image',
                            )
                        )

        # Download thumbnail and save it locally.
        resp, image = http_client.request(thumbnail_remote_url)

        if 'ServiceException' in image or resp.status < 200 or resp.status > 299:
            msg = 'Unable to obtain thumbnail: %s' % image
            logger.debug(msg)
            # Replace error message with None.
            image = None

    if image is not None:
        from geonode.base.models import Thumbnail
        if instance.has_thumbnail():
            instance.thumbnail.thumb_file.delete()
        else:
            thumb = Thumbnail()
            thumb.save()
            instance.thumbnail = thumb
        
        instance.thumbnail.thumb_file.save('layer-%s-thumb.png' % instance.id, ContentFile(image))
        instance.thumbnail.thumb_spec = thumbnail_remote_url
        instance.thumbnail.save()
        instance.save()

        thumbnail_url = urljoin(settings.SITEURL, instance.thumbnail.thumb_file.url)

        Link.objects.get_or_create(resource= instance.resourcebase_ptr,
                        url=thumbnail_url,
                        defaults=dict(
                            name=_('Thumbnail'),
                            extension='png',
                            mime='image/png',
                            link_type='image',
                            )
                        )
