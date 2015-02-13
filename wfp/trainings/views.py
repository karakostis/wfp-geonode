import collections

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from models import Training

def trainings_list(request, template='trainings/training_list.html', **kw):
    
    results = Training.objects.all()
    # get the keywords and their count
    tags = cache.get('training_tags')
    # TODO if not tags:
    # cache tags
    if True:
        tags = {}
        for item in results:
            for tagged_item in item.tagged_items.all():
                tags[tagged_item.tag.slug] = tags.get(tagged_item.tag.slug,{})
                tags[tagged_item.tag.slug]['slug'] = tagged_item.tag.slug
                tags[tagged_item.tag.slug]['name'] = tagged_item.tag.name
                tags[tagged_item.tag.slug]['count'] = tags[tagged_item.tag.slug].get('count',0) + 1
        tags = collections.OrderedDict(sorted(tags.items()))
        cache.set('training_tags', tags)
    
    return render_to_response(template, RequestContext(request, {
        'object_list': results,
        'tags': tags,
    }))
    
def training_detail(request, id):
    """
    The view that show details of each training
    """
    training = get_object_or_404(Training, pk=id)

    return render_to_response("trainings/training_detail.html", 
      RequestContext(request, {
        'training': training
    }))
