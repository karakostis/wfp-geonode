import collections

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from models import Training
from utils import update_training_cache

def trainings_browse(request, keyword = None):
    
    if keyword is not None:
        results = Training.objects.filter(keywords__name = keyword)
    else:
        results = Training.objects.all()

    # get the keywords and their count
    tags = cache.get('training_tags')
    if not tags:
        tags = {}
        for item in Training.objects.all():
            for tagged_item in item.tagged_items.all():
                tags[tagged_item.tag.slug] = tags.get(tagged_item.tag.slug,{})
                tags[tagged_item.tag.slug]['slug'] = tagged_item.tag.slug
                tags[tagged_item.tag.slug]['name'] = tagged_item.tag.name
                tags[tagged_item.tag.slug]['count'] = tags[tagged_item.tag.slug].get('count',0) + 1
        tags = collections.OrderedDict(sorted(tags.items()))
        print tags
        cache.set('training_tags', tags, 60)
    
    return render_to_response('trainings/training_list.html', RequestContext(request, {
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
