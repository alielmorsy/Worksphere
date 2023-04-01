from django.shortcuts import render , HttpResponse  
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt import views as jwt_views
import jwt
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
from datetime import datetime
from django.conf import settings
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer , TokenVerifySerializer 
from rest_framework_simplejwt.views import TokenObtainPairView , TokenVerifyView
from rest_framework_simplejwt.backends import TokenBackend
@method_decorator(csrf_exempt , name='post')
class Login1(View):
    def get(self, request):
        return HttpResponse(request)
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            payload = {
                'user_id': user._id,
                'exp': datetime.now(),
                'token_type': 'access'
            }

            user = {
                'user': username,
                'email': user.email,
                'time': datetime.now().time(),
            }

            token = jwt.encode(payload, settings.SECRET_KEY).decode('utf-8')
            print(token)
            return JsonResponse({'success': 'true', 'token': token, 'user': user})

        else:
            return JsonResponse({'success': 'false', 'msg': 'The credentials provided are invalid.'})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['user'] = self.user.username
        return data

class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def get_user(request , token):
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        print(valid_data)
        user = valid_data['user_id']
        request.user = user
    except:
        print("validation error")

class myverifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        request = self.context.get('request', None)
        data = request.data
        print(request.data)
        get_user(request , data['token'])

        data = super(myverifySerializer, self).validate(attrs)
        data.update({'fullname': request.user})
        return data

class verify(TokenVerifyView):
    serializer_class = myverifySerializer

        
        
