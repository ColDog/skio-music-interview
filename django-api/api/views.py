from django.http import HttpResponse
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import bcrypt
import jwt
from skio.settings import SECRET_KEY
import sys


class AuthenticationFailed(Exception):
    pass


class Controller:
    @classmethod
    def json_response(cls, message, status):
        serialized = json.dumps(message)
        return HttpResponse(serialized, status=status, content_type='application/json')

    @classmethod
    def run_response(cls, method, request, kwargs):
        try:
            return cls.json_response(method(request, kwargs), 200)
        except ObjectDoesNotExist as error:
            message = {'message': error.message, 'success': False}
            return cls.json_response(message, 404)
        except ValidationError as error:
            message = {'message': error.message, 'success': False}
            return cls.json_response(message, 400)
        except IntegrityError as error:
            message = {'message': error.message, 'success': False}
            return cls.json_response(message, 400)
        except AuthenticationFailed as error:
            message = {'message': error.message, 'success': False}
            return cls.json_response(message, 401)
        # can provide json error messages in production.
        # except Exception as error:
        #     message = {'message': error.message, 'success': False}
        #     return json_response(message, 500)


class ApiAuthenticationController(Controller):
    def __init__(self, user_model):
        self.user_model = user_model

    @csrf_exempt
    def authenticate(self, request, **params):
        return self.run_response(self.check_password, request, params)

    def check_password(self, request, params):
        email = request.data.get('email', False)
        password = request.data.get('password', False)
        if email and password:
            user = self.user_model.objects.get(email=email)
            encoded_pass = password.encode('utf-8')
            encoded_hash = user.password.encode('utf-8')
            if bcrypt.hashpw(encoded_pass, encoded_hash):
                token = jwt.encode({'user_id': user.id}, SECRET_KEY)
                message = {'token': token, 'success': True, 'message': 'Authentication successful.', 'user': user._data.to_dict}
                return message
            else:
                raise AuthenticationFailed('Authentication failed.')
        else:
            raise AuthenticationFailed('Authentication failed. No email or password provided.')


class ApiController(Controller):
    def __init__(self, model, **kwargs):
        self.model = model
        self.parent_model = kwargs.get('parent_model', False)
        self.safe_fields = kwargs.get('safe_fields', False) or [field.name for field in self.model._meta.local_fields]
        if self.parent_model:
            self.parent_id = kwargs.get('parent_name', 'parent') + '_id'
        self.model_id = kwargs.get('model_name', 'model') + '_id'
        self.model_set = kwargs.get('model_name', 'model') + '_set'

    def filtered_data(self, request):
        obj = {}
        for key in self.safe_fields:
            if request.data.get(key, False):
                obj[key] = request.data.get(key)
        return obj

    @csrf_exempt
    def nested_all(self, request, **kwargs):
        if request.method == 'POST':
            return self.run_response(self.create, request, kwargs)
        else:
            return self.run_response(self.nested_list, request, kwargs)

    @csrf_exempt
    def all(self, request, **kwargs):
        if request.method == 'POST':
            return self.run_response(self.create, request, kwargs)
        else:
            return self.run_response(self.list, request, kwargs)

    @csrf_exempt
    def all_or_authenticate(self, request, **kwargs):
        if request.method == 'POST':
            return self.run_response(self.create_user, request, kwargs)
        else:
            return self.run_response(self.list, request, kwargs)

    @csrf_exempt
    def single(self, request, **kwargs):
        if request.method == 'POST' or request.method == 'PATCH' or request.method == 'PUT':
            return self.run_response(self.update, request, kwargs)
        elif request.method == 'DELETE':
            return self.run_response(self.destroy, request, kwargs)
        else:
            return self.run_response(self.show, request, kwargs)

    def create_record(self, request, params):
        attrs = self.filtered_data(request)

        if self.parent_model:
            attrs[self.parent_id] = params.get(self.parent_id, None)
        record = self.model(**attrs)
        record.save()
        return record

    def create_user(self, request, params):
        user = self.create_record(request, params)
        token = jwt.encode({'user_id': user.id}, SECRET_KEY)
        return {'success': True, 'token': token, 'user': user._data.to_dict()}

    def create(self, request, params):
        return self.create_record(request, params)._data.to_dict()

    def update(self, request, params):
        filtered = self.model.objects.filter(pk=params.get(self.model_id))
        filtered.update(**self.filtered_data(request))
        return filtered[0]._data.to_dict()

    def destroy(self, request, params):
        record = self.model.objects.get(pk=params.get(params.get(self.model_id)))
        record.delete()
        return {'status': 'success', 'message': 'Record deleted.'}

    def list(self, request, params):
        return [model._data.to_dict() for model in self.model.objects.all()]

    def nested_list(self, request, params):
        parent = self.parent_model.objects.get(pk=params.get(self.parent_id))
        return parent._data.get_relation_as_dict(self.model_set)

    def show(self, request, params):
        record = self.model.objects.get(pk=params[self.model_id])
        return record._data.to_dict_with_relations()
