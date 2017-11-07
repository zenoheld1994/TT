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
from TT.settings import OAUTH2_PROVIDER,SERVER_IP,BASIC_TOKEN
import requests
class SuperAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        idp = request.user.pk
        admin = UserAuth.objects.filter(id=idp,is_superuser=True).exists()
        return admin
class ProfesorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        idp = request.user.pk
        #profesor = UserAuth.objects.filter(id=idp,is_superuser=False).exists()
        profesor = Usuarios.objects.filter(idUser=idp,tipoUsuario=True).exists()
        return profesor

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
					#peticion token
					username=valid.get('usuario')
					password=valid.get('contrasena')
					url = "http://"+SERVER_IP + "/o/token/"
					payload = "grant_type=password&password="+password+"&username="+username
					headers = {
					'content-type': "application/x-www-form-urlencoded",
					'authorization': "Basic "+BASIC_TOKEN,
					'cache-control': "no-cache",
					'postman-token': "cba85345-7c4f-f0fc-c3f3-f2e86bfca26c"
					}
					try:
						response = requests.request("POST", url, data=payload, headers=headers)
					except:
						return Response("0")

					token_json = response.json()
					try:
						serResp["token"] = token_json["access_token"]
						return Response(token_json["access_token"])
					except:
						return Response("0")
					
				else:
					return Response("0")
			else:
				return Response("0")
		else:
			return Response("0")

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
	@list_route(methods=['POST'], permission_classes=[ProfesorPermission])
	def assignGrupo(self,request):
		ser = GrupoSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.assign(request.data,auxid=request.user.pk)
		return Response(result)


class LeccionViewSet(mixins.ListModelMixin,	
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = LeccionSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Leccion.objects.all()
	@list_route(methods=['POST'], permission_classes=[SuperAdminPermission])
	def createLeccion(self,request):
		ser = LeccionSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.create(request.data)
		return Response(result)
	#WS que saque la leccion con el nombre y solo requira el bearer mas el id de leccion
	

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
	def create(self,request):
		ser = PuntuacionSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.create(validated_data=request.data,auxid=request.user.pk)
		return Response(result)
	@list_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated])
	def getPuntuacionbyAlumno(self,request):
		id=request.GET['leccion']
		ser = UserInformation(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.getPuntuaciones(validated_data=request.data,auxid=request.user.pk,leccion=id)
		
		return Response(result)
	@list_route(methods=['GET'], permission_classes=[ProfesorPermission])
	def getPuntuacionesofAlumnoforProfesor(self,request):
		leccion=request.GET['leccion']
		id=request.GET['id']
		ser = UserInformation(data=request.data)
		ser.is_valid(raise_exception=True)
		result = ser.getPuntuacionesofAlumnoforProfesor(validated_data=request.data,auxid=id,idleccion=leccion)
		return Response(result)
	@list_route(methods=['GET'], permission_classes=[ProfesorPermission])
	def getAlumnosbyGrupo(self,request):
		id=request.GET['id']
		alumnos = Usuarios.objects.filter(idGrupo=id,tipoUsuario=False)
		result = UsuarioSerializer(alumnos,many=True).data
		return Response(result)
	#falta el que el wey mande su id y le devuelva su puntuacion yo digo que con un get
	'''
	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def registerPuntuacion(self,request):
		ser = PuntuacionSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		return 
	'''

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
		profesor = UsuarioCreateSerializer2(data=request.data)
		profesor.is_valid(raise_exception=True)
		result = profesor.create(request.data)
		return Response(result)

	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def createAlumno(self, request):
		profesor = UsuarioCreateSerializer3(data=request.data)
		profesor.is_valid(raise_exception=True)
		result = profesor.create(request.data)
		return Response(result)



	@list_route(methods=['GET'], permission_classes=[permissions.AllowAny])
	def getGruposbyProfesorId(self, request):
		try:	
			id=request.GET['id']
			profesores = Usuarios.objects.filter(idEscuela=id,tipoUsuario=True)
			grupos = []
			for y in profesores:
				grupos.append(Grupos.objects.get(idGrupo=y.idGrupo.idGrupo))
			sergrupos = GrupoSerializer(grupos,many=True)
			return Response(sergrupos.data)
		except:
			error={}
			error['error']="ID is required or ID is none"
			return Response(error)
	#falta sacar grupos para profsores por escuela