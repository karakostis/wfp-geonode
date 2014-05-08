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
                if type(value) == type({}):
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
