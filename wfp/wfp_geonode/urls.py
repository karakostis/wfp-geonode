from tastypie.api import Api

from .api import WfpProfileResource

api = Api(api_name='api')
api.register(WfpProfileResource())
