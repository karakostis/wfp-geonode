from django.template import RequestContext
from django.shortcuts import render_to_response

from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.search.views import search_api
from geonode.search.search import _filter_security

def index(request, template='index.html'):
    post = request.POST.copy()
    post.update({'type': 'layer'})
    request.POST = post
    return search_page(request, template=template)


def search_page(request, template='search/search.html', **kw): 
    results, facets, query = search_api(request, format='html', **kw)

    facets = {      
        'maps' : Map.objects.count(),
        'layers' : Layer.objects.count(),
        'documents': Document.objects.count(),
        'users' : Profile.objects.count()
    }
    
    featured_maps = Map.objects.filter(keywords__name__in=['featured'])
    featured_maps = _filter_security(featured_maps, request.user, Map, 'view_map').order_by('data_quality_statement')[:4]
    
    return render_to_response(template, RequestContext(request, {'object_list': results, 
        'facets': facets, 'total': facets['layers'], 'featured_maps': featured_maps }))
