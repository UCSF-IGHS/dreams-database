import json

from rest_framework import renderers

class InterventionRenderer(renderers.JSONRenderer):
    
    def render(self, data, accepted_media_types=None, renderer_context=None):
        response = None

        if 'ErrorDetail' in  str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})