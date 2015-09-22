from urlparse import urlparse, parse_qs
import jwt
from skio.settings import SECRET_KEY
from django.http import HttpResponse
import json
from api.models import User
import re
import json
import sys
from api.urls import PROTECTED_ROUTES


class ApiAuthenticationMiddleware:
    def process_request(self, request):

        request.params = parse_qs(urlparse(request.META.get('QUERY_STRING')).query)

        request.data = {}

        for key in request.POST:
            request.data[key] = request.POST[key]

        try:
            request.data.update(json.loads(request.body))
        except ValueError as er:
            print >>sys.stderr, 'value error', er

        print >>sys.stderr, 'DATA:', request.data, request.params

        def search_route(method, url):
            matchers = []
            matchers.extend(PROTECTED_ROUTES.get(method, []))
            matchers.extend(PROTECTED_ROUTES.get('ALL', []))
            for match in matchers:
                if re.search(match, url):
                    return True
            return False

        if search_route(request.method, request.path):
            token = request.data.get('access-token') or \
                    request.META.get('X-ACCESS-TOKEN') or \
                    request.META.get('x-access-token') or \
                    request.params.get('access-token')

            if token:
                try:
                    decoded = jwt.decode(token, SECRET_KEY)
                    request.user = User.objects.get(pk=decoded.user_id)
                    return None
                except jwt.InvalidTokenError:
                    message = json.dumps({'success': False, 'message': 'Failed to validate with the given credentials.'})
                    return HttpResponse(message, status=401)
            else:
                message = json.dumps({'success': False, 'message': 'Failed to validate, no credentials were provided.'})
                return HttpResponse(message, status=401)
        else:
            return None
