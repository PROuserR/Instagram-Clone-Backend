from django.contrib.auth import logout
from django.contrib.auth.models import User, update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from .serializers import *


@api_view(['POST'])
def register_user(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    
    user = User.objects.create_user(username, email, password)

    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data['id'])
    else:
        return Response('Register error')


@api_view(['GET'])
def user_last_login_update(request, user_id):
    user = User.objects.get(id=user_id)
    update_last_login(None, user)
    return Response({'userLastLogin': user.last_login})

    
@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response('Logout')


@api_view(['GET'])
def generate_token(request, username):
    try:
        token = Token.objects.create(user=User.objects.get(username=username))
        return Response(token.key)
    except:
        token = Token.objects.get(user=User.objects.get(username=username))
        return Response(token.key)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    data = request.data
    data['password'] = user.password
    serializer = UserSerializer(instance=user, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
        
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def update_password(request):
    user = request.user
    user.set_password(request.data['password'])
    user.save()
    return Response('Password changed')