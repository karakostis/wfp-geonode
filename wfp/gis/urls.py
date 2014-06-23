from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView

from tastypie.api import Api

from api import OfficeResource, EmployeeResource

v1_api = Api(api_name='v1')
v1_api.register(OfficeResource())
v1_api.register(EmployeeResource())

urlpatterns = patterns(
    'wfp.gis.views',
    url(r'^api/', include(v1_api.urls)),
    url(r'^employees-map/$', TemplateView.as_view(template_name='gis/employees-map.html')),
)
