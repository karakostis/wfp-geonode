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

import json

from django.http import HttpResponse

from wfp import get_version

from django.conf import settings

def wfp_geonode(request):
    """ Global values related to WFPGeoNode to pass to templates """
    return dict(
        WFPGEONODE_VERSION=get_version(),
    )

def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    ga_prop_id = settings.GOOGLE_ANALYTICS_ID
    if ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_ID': ga_prop_id,
        }
    return {}

def google_form(request):
    return {'GOOGLE_FORM_LINK': settings.GOOGLE_FORM_LINK}

class NonHtmlDebugToolbarMiddleware(object):
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    @staticmethod
    def process_response(request, response):
        if request.GET.get('debug') == '':
            if response['Content-Type'] == 'application/octet-stream':
                new_content = '<html><body>Binary Data, ' \
                    'Length: {}</body></html>'.format(len(response.content))
                response = HttpResponse(new_content)
            elif response['Content-Type'] != 'text/html':
                content = response.content
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse('<html><body><pre>{}'
                                        '</pre></body></html>'.format(content))

        return response
