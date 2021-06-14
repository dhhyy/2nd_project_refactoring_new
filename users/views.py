import re
import bcrypt
import jwt
import json
import requests

from django.views import View
from django.http import HttpResponse, JsonResponse, response
from .models import User, Coupon, UserCoupon
from .utils import LoginDecorator
from my_settings import SECRET_KEY, email_validation, password_validation, algorithm

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email          = data['email'] 
            password       = data['password']
            password_check = data['password_check']
            name           = data['name']
        
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EXIST_EMAIL'}, status=400)

            if not password == password_check:
                return JsonResponse({'message' : 'CHECK_YOUR_INPUT'}, status=400)

            if not email_validation.match(email):
                return JsonResponse({'message' : 'NOT_MATCHED_EMAIL_FORM'}, status=400)

            if not password_validation.match(password):
                return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD_FORM'}, status=400)
        
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
            User.objects.create(
                    email = email, 
                    password = hashed_password,
                    name = name
                    )

            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except KeyError:    
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            if not email or not password:
                return JsonResponse({'message' : 'CHECK_YOUR_INPUT'}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'NOT_MATCHED_EMAIL'}, status=400)
        
            user_email = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user_email.password.encode('-utf-8')):
                access_token = jwt.encode({'id' : user_email.id}, SECRET_KEY, algorithm)
            
                return JsonResponse({'access_token' : access_token, 'message' : 'SUCCESS'}, status=200)

            return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class Example(View):
    @LoginDecorator
    def post(self, request):
        
        try:    
            user = User.objects.get(id = 1)
            return JsonResponse({'user_name' : user.name}, status=200)
        
        except:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class KakaoSignInView(View):
    def post(self, request):
        
        try:
            access_token = request.headers['Authorization']
            # access_token  = "2gJFIyZBcO_yLeY5eb-MwuPIdU9FojSjeOjSSgo9dRoAAAF5rLbxTA"
            url           = 'https://kapi.kakao.com/v2/user/me'
            header        = {'Authorization' : f'Bearer {access_token}'}
            response      = requests.post(url, headers=header)
            
            data = response.json()
            
            if not data.get('id'):
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
            
            user, create = User.objects.get_or_create(
                is_social = data['id'],
                email     = data['kakao_account']['email'],
                name      = data['properties']['nickname']
            )
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm)

            print(access_token)
            
            return JsonResponse({'access_token' : access_token}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)