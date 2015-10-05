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

from tastypie.serializers import Serializer
import json
from django.core.serializers.json import DjangoJSONEncoder


class GeoJSONSerializer(Serializer):
    """
    Custom GeoJSON tastypie serializer.
    Based on (with some improvements:
    https://github.com/toastdriven/django-tastypie/issues/1022
    """

    def to_geojson(self, data, options=None):
        """
        Given some Python data, produces GeoJSON output.
        """

        def _build_feature(obj):
            f = {
                "type": "Feature",
                "properties": {}
            }

            def recurse(key, value):
                if key in ['id', 'geometry']:
                    f[key] = value
                    return
                if key == 'resource_uri':
                    return
                if isinstance(value, dict):
                    for k in value:
                        recurse(k, value[k])
                else:
                    f['properties'][key] = unicode(value)

            for key, value in obj.iteritems():
                recurse(key, value)
            return f

        def _build_feature_collection(objs, meta):
            fc = {
                "type": "FeatureCollection",
                "features": []
            }
            if(meta):
                fc["meta"] = meta
            for obj in objs:
                fc['features'].append(_build_feature(obj))
            return fc

        options = options or {}
        data = self.to_simple(data, options)
        meta = data.get('meta')
        if 'objects' in data:
            data = _build_feature_collection(data['objects'], meta)
        else:
            data = _build_feature(data)
        return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)

    def to_json(self, data, options=None):
        """
        Override to enable GeoJSON generation when the geojson option is passed.
        """
        options = options or {}
        if options.get('geojson'):
            return self.to_geojson(data, options)
        else:
            return super(GeoJSONSerializer, self).to_json(data, options)
