#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import collections
import json
import logging

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required

from geonode.utils import http_client
from geonode.geoserver.helpers import OGC_Servers_Handler

from models import Training
from forms import TrainingForm

logger = logging.getLogger("wfp.trainings.views")
ogc_server_settings = OGC_Servers_Handler(settings.OGC_SERVER)['default']


def trainings_browse(request, keyword=None):
    """
    Browse the trainings list.
    """
    if keyword is not None:
        results = Training.objects.filter(keywords__name=keyword)
    else:
        results = Training.objects.all()

    # get the keywords and their count
    tags = cache.get('training_tags')
    if not tags:
        tags = {}
        for item in Training.objects.all():
            for tagged_item in item.tagged_items.all():
                tags[tagged_item.tag.slug] = tags.get(tagged_item.tag.slug, {})
                tags[tagged_item.tag.slug]['slug'] = tagged_item.tag.slug
                tags[tagged_item.tag.slug]['name'] = tagged_item.tag.name
                tags[tagged_item.tag.slug]['count'] = (
                    tags[tagged_item.tag.slug].get('count', 0) + 1)
        tags = collections.OrderedDict(sorted(tags.items()))
        cache.set('training_tags', tags, 60)

    return render_to_response(
        'trainings/training_list.html',
        RequestContext(request, {
            'object_list': results,
            'tags': tags,
        })
    )


def training_detail(request, id):
    """
    Show the details of each training
    """
    training = get_object_or_404(Training, pk=id)

    return render_to_response(
        'trainings/training_detail.html',
        RequestContext(request, {'training': training})
    )


@permission_required('trainings.add_training')
def training_upload(request):
    """
    Upload a new training
    """
    if request.method == 'GET':
        form = TrainingForm()
    else:
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save()
            return HttpResponseRedirect(
                reverse('training_detail', kwargs={'id': training.id})
            )

    return render_to_response(
        'trainings/training_upload.html',
        RequestContext(request, {'form': form})
    )


def training_download(
        request, id,
        template='trainings/training_download.html'):
    """
    Download all the layers of a training as a batch
    """
    training = get_object_or_404(Training, pk=id)

    training_status = dict()
    if request.method == 'POST':
        url = ("%srest/process/batchDownload/launch/"
               % ogc_server_settings.LOCATION)

        def perm_filter(layer):
            return request.user.has_perm('layers.view_layer', obj=layer)

        # here we build the json necessary to the rest batchDownload
        data = {
                 'layers': [],
                 "map": {
                         'readme': training.abstract,
                         'title': training.title
                       }
               }
        for layer in training.layers.all():
            store_type = 'WFS'
            if layer.storeType == 'coverageStore':
                store_type = 'WCS'
            layer_data = {
                           'metadataURL': '',
                           'service': store_type,
                           'name': layer.typename,
                           'serviceURL': ''
                         }
            data['layers'].append(layer_data)

        training_json = json.dumps(data)

        resp, content = http_client.request(url, 'POST', body=training_json)

        status = int(resp.status)

        if status == 200:
            training_status = json.loads(content)
            request.session["training_status"] = training_status
        else:
            raise Exception(
                'Could not start the download of %s. Error was: %s' %
                (training.title, content)
            )

    downloadable_layers = []
    for layer in training.layers.all():
        if request.user.has_perm('layers.view_layer', obj=layer):
            downloadable_layers.append(layer)

    return render_to_response(template, RequestContext(request, {
         "training_status": training_status,
         "training": training,
         "downloadable_layers": downloadable_layers,
         "geoserver": ogc_server_settings.public_url,
         "site": settings.SITEURL
    }))


def training_download_check(request):
    """
    Endpoint for monitoring training downloads
    """
    try:
        layer = request.session["training_status"]
        if type(layer) == dict:
            url = (
                "%srest/process/batchDownload/status/%s" %
                (ogc_server_settings.LOCATION, layer["id"])
            )
            resp, content = http_client.request(url, 'GET')
            status = resp.status
            if resp.status == 400:
                return HttpResponse(
                    content="Something went wrong",
                    status=status
                )
        else:
            content = "Something Went wrong"
            status = 400
    except ValueError:
        # TODO: Is there any useful context we could include in this log?
        logger.warn(
            'User tried to check status, but has no download in progress.'
        )
    return HttpResponse(content=content, status=status)
