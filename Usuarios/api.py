#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import viewsets, status, mixins, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, \
	TokenHasScope, OAuth2Authentication
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User as UserAuth
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login, get_user_model
from uuid import uuid4
from django.http import HttpResponse
import json 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
class SuperAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        idp = request.user.pk
        admin = UserAuth.objects.filter(id=idp,is_superuser=True).exists()
        return admin

class UsuariosViewSet(mixins.ListModelMixin,
	#mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = UsuarioSerializer
	permission_classes = [SuperAdminPermission, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Usuarios.objects.all()

	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def createUsuario(self, request):
		usuario = UsuarioCreateSerializer(data=request.data)
		usuario.is_valid(raise_exception=True)
		result = usuario.create(request.data)
		return Response(result)
	#Check permissions for this one
	@list_route(methods=['PATCH'], permission_classes=[permissions.AllowAny])
	def updateUsuario(self, request):
		usuario = UsuarioUpdateSerializer(data=request.data)
		usuario.is_valid(raise_exception=True)
		result = usuario.update(request.data)
		return Response(result)
	@list_route(methods=['GET'], permission_classes=[SuperAdminPermission])
	def getUsuarios(self, request):
		usuarios = Usuarios.objects.all()
		seruser = UsuarioSerializer(usuarios,many=True)
		
		return Response(seruser.data)

	@csrf_exempt
	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def login(self, request):
		serializer = UsuarioLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		valid = serializer.validated_data
		if (valid.get('usuario') is not None):
			userModel = get_object_or_404(UserAuth, username=valid.get('usuario'))
			if userModel.is_active:
				try:
					
					user = UserAuth.objects.get(id=userModel.id)
				except:
					return Response({'detail': "464"}, status=status.HTTP_401_UNAUTHORIZED,
								content_type="applicationjson")

				userAuth = authenticate(username=valid.get('usuario'),
										password=valid.get('contrasena'))
				if userAuth is not None:
					login(request, userAuth)
					resp = Usuarios.objects.get(idUser=userModel.id)
					serResp = UsuarioSerializer(resp).data

					return Response(serResp)
				else:
					return Response({'detail': "461"}, status=status.HTTP_401_UNAUTHORIZED)
			else:
				return Response({'detail': "443"}, status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({'detail': "464"}, status=status.HTTP_401_UNAUTHORIZED)

class EscuelasViewSet(mixins.ListModelMixin,
	mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = EscuelaSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Escuelas.objects.all()
	@list_route(methods=['GET'], permission_classes=[SuperAdminPermission])
	def getEscuelas(self, request):
		escuelas = Escuelas.objects.all()
		serescuela = EscuelaSerializer(escuelas,many=True)
		return Response(serescuela.data)


class GruposViewSet(mixins.ListModelMixin,
	mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = GrupoSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Grupos.objects.all()
	def create(self,request):
		ser = GrupoSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.create(request.data,auxid=request.user.pk)
		return Response(result)


class LeccionViewSet(mixins.ListModelMixin,
	mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = LeccionSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Leccion.objects.all()

class PuntuacionViewSet(mixins.ListModelMixin,
	mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = PuntuacionSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Puntuaciones.objects.all()

class EveryoneViewSet(mixins.ListModelMixin,
	mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet):
	serializer_class = UsuarioSerializer
	authentication_classes = [OAuth2Authentication]
	queryset = Usuarios.objects.all()
	@list_route(methods=['GET'], permission_classes=[permissions.AllowAny])
	def getEscuelas(self, request):
		escuelas = Escuelas.objects.all()
		serescuelas = EscuelaSerializer(escuelas,many=True)
		return Response(serescuelas.data)
	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def createProfesor(self, request):
		profesor = UsuarioCreateSerializer(data=request.data)
		profesor.is_valid(raise_exception=True)
		result = profesor.create(request.data)
		return Response(result)
