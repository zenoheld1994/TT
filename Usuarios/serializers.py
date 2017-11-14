#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User as UserAuth
import re
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from oauth2_provider.models import Application
from .models import Escuelas,Leccion,Usuarios,Puntuaciones,Grupos

class UsuarioSerializer(serializers.Serializer):
	idUsuario = serializers.IntegerField(required=True)
	tipoUsuario = serializers.BooleanField(required=True)
	usuario = serializers.SerializerMethodField()
	nombre = serializers.CharField(required=True)
	idUser = serializers.IntegerField(required=True)
	idEscuela = serializers.SerializerMethodField()
	idGrupo = serializers.SerializerMethodField()
	nombreGrupo = serializers.SerializerMethodField()
	nombreEscuela = serializers.SerializerMethodField()
	class Meta:
		model = Usuarios
		fields = ('tipoUsuario','usuario','nombre','idEscuela','idUsuario','idUser')
	def get_idEscuela(self,obj):
		return obj.idEscuela.pk
	def get_usuario(self,obj):
		userauth = UserAuth.objects.get(pk=obj.idUser)
		return userauth.username
	def get_idGrupo(self,obj):
		try:
			return obj.idGrupo.pk
		except:
			try:
				return obj.idGrupo
			except:
				return None
	def get_nombreGrupo(self,obj):
		try:
			grupo = Grupos.objects.get(pk=obj.idGrupo.pk)
			return grupo.nombre
		except:
			try:
				grupo = Grupos.objects.get(pk=obj.idGrupo)
				return grupo.nombre
			except:
				return None
	def get_nombreEscuela(self,obj):
		try:
			escuela = Escuelas.objects.get(pk=obj.idEscuela.pk)
			return escuela.nombre
		except:
			try:
				escuela = Escuelas.objects.get(pk=obj.idEscuela)
				return escuela.nombre
			except:
				return None


class UsuarioLoginSerializer(serializers.Serializer):
	usuario = serializers.CharField(required=True)
	contrasena = serializers.CharField(required=True)
	class Meta:
		model = Usuarios
		fields = ('usuario','contrasena')

class UsuarioCreateSerializer(serializers.Serializer):
	tipoUsuario = serializers.BooleanField(required=True)
	usuario = serializers.CharField(required=True)
	contrasena = serializers.CharField(required=True)
	nombre = serializers.CharField(required=True)
	idEscuela = serializers.IntegerField(required=True)
	class Meta:
		model = Usuarios
		fields = ('tipoUsuario','usuario','contrasena','nombre','idEscuela')
	def validate_contrasena(self,value):
		algo = re.match('\w{5}',value)
		if algo:
		   return value
		else:
			raise serializers.ValidationError("Password's length must be at least 5 characters")
	def validate_usuario(self,value):
		if UserAuth.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists")
		return value
	def create(self, validated_data):
		#try:
		userauth = UserAuth.objects.create_user(username=self.data.get('usuario'), password=self.data.get('contrasena'),
			is_active=1)
		try:
			escuela_aux = Escuelas.objects.get(pk=self.data.get('idEscuela'))
			usuario = Usuarios(tipoUsuario=self.data.get('tipoUsuario'),
				nombre=self.data.get('nombre'),idUser=userauth.id,
				idEscuela=escuela_aux)
			usuario.save()
		except:
			userauth.delete()
			return "ERROR WHILE CREATING USER"

		return UsuarioSerializer(usuario).data

class UsuarioCreateSerializer2(serializers.Serializer):
	tipoUsuario = serializers.BooleanField(required=True)
	usuario = serializers.CharField(required=True)
	contrasena = serializers.CharField(required=True)
	nombre = serializers.CharField(required=True)
	idEscuela = serializers.IntegerField(required=True)
	nameGrupo = serializers.CharField(required=True)
	class Meta:
		model = Usuarios
		fields = ('tipoUsuario','usuario','contrasena','nombre','idEscuela','nameGrupo')
	def validate_contrasena(self,value):
		algo = re.match('\w{5}',value)
		if algo:
		   return value
		else:
			raise serializers.ValidationError("La contraseña debe ser de al menos 5 caracteres")
	def validate_usuario(self,value):
		if UserAuth.objects.filter(username=value).exists():
			raise serializers.ValidationError("El usuario ya existe use otro")
		return value
	def create(self, validated_data):
		try:
			userauth = UserAuth.objects.create_user(username=self.data.get('usuario'), password=self.data.get('contrasena'),
				is_active=1)
			try:
				escuela_aux = Escuelas.objects.get(pk=self.data.get('idEscuela'))
				grupo = Grupos.objects.create(nombre=self.data.get('nameGrupo'))
				usuario = Usuarios(tipoUsuario=self.data.get('tipoUsuario'),
					nombre=self.data.get('nombre'),idUser=userauth.id,
					idEscuela=escuela_aux,idGrupo=grupo)
				usuario.save()
			except:
				userauth.delete()
				return "ERROR WHILE CREATING USER"
		except:
			userauth.delete()
			return "ERROR WHILE CREATING USER"
		return UsuarioSerializer(usuario).data

class UsuarioCreateSerializer3(serializers.Serializer):
	usuario = serializers.CharField(required=True)
	contrasena = serializers.CharField(required=True)
	nombre = serializers.CharField(required=True)
	idEscuela = serializers.IntegerField(required=True)
	grupo = serializers.IntegerField(required=True)
	class Meta:
		model = Usuarios
		fields = ('usuario','contrasena','nombre','idEscuela','grupo')
	def validate_contrasena(self,value):
		algo = re.match('\w{5}',value)
		if algo:
		   return value
		else:
			raise serializers.ValidationError("La contraseña debe ser de al menos 5 caracteres")
	def validate_usuario(self,value):
		if UserAuth.objects.filter(username=value).exists():
			raise serializers.ValidationError("El usuario ya existe use otro")
		return value
	def create(self, validated_data):
		try:
			userauth = UserAuth.objects.create_user(username=self.data.get('usuario'), password=self.data.get('contrasena'),
				is_active=1)
			try:
				escuela_aux = Escuelas.objects.get(pk=self.data.get('idEscuela'))
				grupo = Grupos.objects.get(idGrupo=self.data.get('grupo'))
				usuario = Usuarios(tipoUsuario=False,
					nombre=self.data.get('nombre'),idUser=userauth.id,
					idEscuela=escuela_aux,idGrupo=grupo)
				usuario.save()
			except:
				userauth.delete()
				return "ERROR WHILE CREATING USER"
		except:
			userauth.delete()
			return "ERROR WHILE CREATING USER"
		return UsuarioSerializer(usuario).data


class UsuarioUpdateSerializer(serializers.Serializer):
	contrasena = serializers.CharField(required=False)
	nombre = serializers.CharField(required=False)
	usuario = serializers.CharField(required=False)
	#idUsuario = serializers.IntegerField(required=True)
	idGrupo = serializers.CharField(required=False)
	#de mientras se enablea el oauth2
	class Meta:
		model = Usuarios
		fields = ('idUser','contrasena','nombre','usuario')
	def validate_contrasena(self,value):
		algo = re.match('\w{8}',value)
		if algo:
		   return value
		else:
			raise serializers.ValidationError("Password's length must be at least 8 characters")
	def validate_usuario(self,value):
		if UserAuth.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists")
		return value
	def update(self, validated_data,auxid):
		instance = Usuarios.objects.get(idUser=auxid)
		userauth = UserAuth.objects.get(pk=instance.idUser)
		
		try:
			userauth.username=self.data.get('usuario')
			userauth.save()
		except:
			None
		instance.nombre = validated_data.get('nombre',instance.nombre)
		instance.save()
		return UsuarioSerializer(instance).data

class UsuarioDeleteSerializer(serializers.Serializer):
	idUsuario = serializers.IntegerField(required=True)
	#de mientras se enablea el oauth2
	class Meta:
		model = Usuarios
		fields = ('iUsuario')

	def delete(self, validated_data):
		usuario = Usuarios.objects.get(pk=self.data.get('idUsuario'))
		userauth = UserAuth.objects.get(pk=instance.idUser)
		try:
			usuario.delete()
			userauth.delete()
		except:
			return "ERROR"
		return "OK"

class EscuelaSerializer(serializers.Serializer):
	idEscuela = serializers.IntegerField(required=False)
	nombre = serializers.CharField(required=True)
	class Meta:
		model = Escuelas
		fields = ('nombre','idEscuela')
	def create(self,validated_data):
		return Escuelas.objects.create(**validated_data)
	def update(self, instance, validated_data):
		instance.nombre = validated_data.get('nombre', instance.nombre)
		instance.save()
		return instance

class EscuelaCreateSerializer(serializers.Serializer):
	nombre = serializers.CharField(required=True)
	class Meta:
		model = Escuelas
		fields = ('__all__')
	def create(self, validated_data):
		escuela = Escuelas(nombre=self.data.get('nombre'))
		escuela.save()
		return EscuelaSerializer(escuela).data
		

class GrupoSerializer(serializers.Serializer):
	nombre = serializers.CharField(required=False)
	idGrupo = serializers.IntegerField(required=False)
	idUsuario = serializers.IntegerField(required=False)
	class Meta:
		model = Grupos
		fields = ('nombre','idGrupo','idUsuario')
	def create(self, validated_data,auxid):
		grupo = Grupos.objects.create(**validated_data)
		user = Usuarios.objects.get(idUser=auxid)
		user.idGrupo = grupo
		user.save()
		return GrupoSerializer(grupo).data
	def update(self, instance, validated_data):
		instance.nombre = validated_data.get('nombre', instance.nombre)
		try:
			auxUser = Usuarios.objects.get(pk=validated_data.get('idUsuario'))
			auxUser.idGrupo = instance
			auxUser.save()
		except:
			None
		instance.save()
		return instance
	def assign(self,validated_data,auxid):
		grupo = Grupos.objects.get(idGrupo=self.data.get('idGrupo'))
		usuario = Usuarios.objects.get(idUser=auxid)
		usuario.idGrupo = grupo
		usuario.save()
		return UsuarioSerializer(usuario).data

		
	

class LeccionSerializer(serializers.Serializer):
	idLeccion = serializers.CharField(required=False)
	nombre = serializers.CharField(required=False)
	maxima = serializers.IntegerField(required=False)
	class Meta:
		model = Leccion
		fields = ('nombre')
	def create(self,validated_data):
		nombre = "Lección "
		try:
			id=Leccion.objects.latest('idLeccion').idLeccion
			id+=1
		except:
			id=1
		try:
			leccion = Leccion.objects.create(nombre=nombre+str(id),idLeccion=id,maxima=self.data.get('maxima'))
		except:
			return "ERROR WHILE CREATING LECCION"
		return LeccionSerializer(leccion).data
	def update(self, instance, validated_data):	
		instance.nombre = validated_data.get('nombre', instance.nombre)
		instance.save()
		return instance
class PuntuacionAuxSerializer(serializers.Serializer):
	idPuntuacion = serializers.IntegerField(required=False)
	puntuacion = serializers.IntegerField(required=False)
	idUsuario = serializers.SerializerMethodField()
	idLeccion = serializers.SerializerMethodField()
	class Meta:
		model = Leccion
		fields = ('idPuntuacion','puntuacion','idUsuario','idLeccion')
	def get_idUsuario(self,obj):
		return obj.idUsuario.pk
	def get_idLeccion(self,obj):
		return obj.idLeccion.pk
class PuntuacionAux2Serializer(serializers.Serializer):
	idPuntuacion = serializers.IntegerField(required=False)
	puntuacion = serializers.IntegerField(required=False)
	class Meta:
		model = Leccion
		fields = ('idPuntuacion','puntuacion')

class PuntuacionSerializer(serializers.Serializer):
	idPuntuacion = serializers.IntegerField(required=False)
	puntuacion = serializers.IntegerField(required=False)
	#idUsuario = serializers.IntegerField()
	idLeccion = serializers.IntegerField()
	class Meta:
		model = Leccion
		fields = ('idPuntuacion','puntuacion','idLeccion')
	def create(self,validated_data,auxid):
		idUsuario_aux = Usuarios.objects.get(idUser=auxid)
		idLeccion_aux = Leccion.objects.get(pk=validated_data.pop('idLeccion'))
		puntuacion_aux = Puntuaciones.objects.create(puntuacion=self.data.get('puntuacion'),idUsuario=idUsuario_aux,idLeccion=idLeccion_aux)
		return PuntuacionAuxSerializer(puntuacion_aux).data

	def update(self, instance, validated_data):
		instance.puntuacion = validated_data.get('puntuacion', instance.puntuacion)
		instance.save()
		return instance

class UserInformation(serializers.Serializer):
	idUsuario = serializers.IntegerField(required=False)
	class Meta:
		model = Usuarios
		fields = ('idUsuario',)
	def getPuntuaciones(self,validated_data,auxid,leccion):
		try:
			idUsuario_aux = Usuarios.objects.get(idUser=auxid,tipoUsuario=False)
			puntuaciones = Puntuaciones.objects.filter(idUsuario=idUsuario_aux.idUsuario,idLeccion=leccion)
			return PuntuacionAux2Serializer(puntuaciones,many=True).data
		except:
			return "Error while retrieving data UserInformation->Método.360 Serializers"
	def getPuntuacionesofAlumno(self,validated_data,auxid):
		idUsuario_aux = Usuarios.objects.get(idUsuario=auxid,tipoUsuario=False)
		puntuaciones = Puntuaciones.objects.filter(idUsuario=idUsuario_aux.idUsuario)
		return PuntuacionAuxSerializer(puntuaciones,many=True).data
	
		return "Error while retrieving data UserInformation->Método.367 Serializers"
	def getPuntuacionesofAlumnoforProfesor(self,validated_data,auxid,idleccion):
		idUsuario_aux = Usuarios.objects.get(idUsuario=auxid,tipoUsuario=False)
		puntuaciones = Puntuaciones.objects.filter(idUsuario=idUsuario_aux.idUsuario,idLeccion=idleccion)
		return PuntuacionAuxSerializer(puntuaciones,many=True).data
	
		return "Error while retrieving data UserInformation->Método.374 Serializers"
