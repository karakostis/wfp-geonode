from urlparse import urlsplit
from httplib import HTTPConnection,HTTPSConnection
import urllib2, base64
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.http.request import validate_host

from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.search.views import search_api
from geonode.search.search import _filter_security
from geonode.utils import ogc_server_settings

from wfp.wfpdocs.models import WFPDocument

def index(request):
    post = request.POST.copy()
    post.update({'type': 'layer'})
    request.POST = post
    return search_page(request, template='site_index.html')

def search_page(request, template='search/search.html', **kw): 
    results, facets, query = search_api(request, format='html', **kw)

    facets = {      
        'maps' : Map.objects.count(),
        'layers' : Layer.objects.count(),
        'wfpdocuments': WFPDocument.objects.count(),
        'users' : Profile.objects.count()
    }
    
    featured_maps = Map.objects.filter(keywords__name__in=['featured'])
    featured_maps = _filter_security(featured_maps, request.user, Map, 'view_map').order_by('data_quality_statement')[:4]
    
    return render_to_response(template, RequestContext(request, {'object_list': results, 
        'facets': facets, 'total': facets['layers'], 'featured_maps': featured_maps }))
    
def contacts(request):
    profiles = Profile.objects.filter(user__groups__name='OMEP GIS Team').order_by('name')
    return render_to_response('contacts.html', 
        {   
            'profiles': profiles,
        },
        context_instance=RequestContext(request))


def apps_proxy(request):
    PROXY_ALLOWED_HOSTS = (ogc_server_settings.hostname,) + getattr(settings, 'PROXY_ALLOWED_HOSTS', ())

    if 'url' in request.GET:
        raw_url = request.GET['url']
    else:
        querystring = urllib2.unquote(request.META['QUERY_STRING'])
        raw_url = '%sows?%s' % (settings.OGC_SERVER['default']['LOCATION'], querystring)
    
    url = urlsplit(raw_url)
    if url is None:
        return HttpResponse(
                "The proxy service requires a URL-encoded URL as a parameter.",
                status=400,
                content_type="text/plain"
                )
                
    if not settings.DEBUG:
        print url.hostname
        if not validate_host(url.hostname, PROXY_ALLOWED_HOSTS):
            return HttpResponse(
                    "DEBUG is set to False but the host of the path provided to the proxy service (%s) is not in the"
                    " PROXY_ALLOWED_HOSTS setting." % url.hostname,
                    status=403,
                    content_type="text/plain"
                    )

    print 'proxying to %s' % raw_url
    proxy_request = urllib2.Request(raw_url)
    base64string = base64.encodestring('%s:%s' % (settings.EXT_APP_USER, settings.EXT_APP_USER_PWD)).replace('\n', '')
    proxy_request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(proxy_request)

    response = HttpResponse(
            result,
            status=result.code,
            content_type=result.headers["Content-Type"]
            )

    return response


def test_proxy(request):
    # todo remove this
    from django.shortcuts import render_to_response
    return render_to_response('test_proxy.html')
