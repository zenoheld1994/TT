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



class UsuariosViewSet(mixins.ListModelMixin,
	#mixins.CreateModelMixin, 
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	#mixins.DestroyModelMixin,
	viewsets.GenericViewSet):
	serializer_class = UsuarioSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Usuarios.objects.all()
	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def createUsuario(self, request):
		usuario = UsuarioCreateSerializer(data=request.data)
		usuario.is_valid(raise_exception=True)
		result = usuario.create(request.data)
		return Response(result)

	def update(self, request):
		usuario = UsuarioUpdateSerializer(data=request.data)
		usuario.is_valid(raise_exception=True)
		result = usuario.update(request.data)
		return Response(result)

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
	@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def createEscuela(self, request):
		escuela = EscuelaCreateSerializer(data=request.data)
		escuela.is_valid(raise_exception=True)
		result = escuela.create(request.data)
		return Response(result)

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
	#@list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
	def create(self, request):
		grupo = GrupoCreateSerializer(data=request.data)
		grupo.is_valid(raise_exception=True)
		result = grupo.create(request.data)
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
	serializer_class = PuntuacionAuxSerializer
	permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	authentication_classes = [OAuth2Authentication]
	queryset = Puntuaciones.objects.all()

#LeccionSerializer