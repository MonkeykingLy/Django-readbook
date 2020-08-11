from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

class User(APIView):

    def post(self, request):
      return Response(status=HTTP_200_OK)
