from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from users.serializers import UserSerialize
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

# Create your views here.


class RegisterView(APIView):
    def post(self,requset):
        serializer = UserSerialize(data=requset.data)
        
        if not serializer.is_valid():
            return Response({
                  'error': serializer.errors
        },status=HTTP_404_NOT_FOUND)
            
        serializer.save()
        return Response(serializer.data,status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email = email).first()


        user_not_found_response =  Response({
                  'error': "User not found!"
        },status=HTTP_404_NOT_FOUND)

        if user is None:
             return user_not_found_response

        if not user.check_password(password):
             return user_not_found_response


        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }    

        token = jwt.encode(payload,'secret',algorithm='HS256')
        return Response({
            'token': token
        })