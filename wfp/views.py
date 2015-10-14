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

from urlparse import urlsplit
import urllib2
import base64
import json
from datetime import date

from django.http import HttpResponse
from django.conf import settings
from django.http.request import validate_host
from django.utils.http import int_to_base36, base36_to_int
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac

from geonode.geoserver.helpers import ogc_server_settings


def _generate_token():
    timestamp = _num_days(date.today())
    ts_b36 = int_to_base36(timestamp)
    key_salt = "geonoed.TokenGenerator"
    value = (settings.EXT_APP_USER + settings.EXT_APP_USER_PWD + six.text_type(timestamp))
    hash = salted_hmac(key_salt, value).hexdigest()[::2]
    return "%s-%s" % (ts_b36, hash)


def _num_days(dt):
    return (dt - date(2001, 1, 1)).days


def _check_token(token):
    # Parse the token
    try:
        ts_b36, hash = token.split("-")
    except ValueError:
        return False

    try:
        ts = base36_to_int(ts_b36)
    except ValueError:
        return False

    # Check that the timestamp/uid has not been tampered with
    if not constant_time_compare(_generate_token(), token):
        return False

    # Check the timestamp is within limit
    daydiff = _num_days(date.today()) - ts
    timeout_days = 1
    if (daydiff) > timeout_days:
        return False

    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_token(request):
    print 'ip is: %s' % get_client_ip(request)
    response_data = {}
    client_ip = get_client_ip(request)
    if client_ip in settings.EXT_APP_IPS:
        token = _generate_token()
    else:
        token = 'Invalid request. IP %s is not in EXT_APP_IPS' % client_ip
    response_data['token'] = token
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def apps_proxy(request):
    PROXY_ALLOWED_HOSTS = (ogc_server_settings.hostname,) + getattr(settings, 'PROXY_ALLOWED_HOSTS', ())

    token = None
    if 'token' in request.GET:
        token = request.GET['token']
    if token is None:
        print "The proxy service requires a token."
        return HttpResponse(
                "The proxy service requires a token.",
                status=400,
                content_type="text/plain"
                )
    if not _check_token(token):
        print "The provided token is invalid."
        return HttpResponse(
                "The provided token is invalid.",
                status=400,
                content_type="text/plain"
                )

    if 'url' in request.GET:
        raw_url = request.GET['url']
    else:
        # querystring = urllib2.unquote(request.META['QUERY_STRING'])
        querystring = request.META['QUERY_STRING']
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
