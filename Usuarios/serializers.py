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
	class Meta:
		model = Usuarios
		fields = ('tipoUsuario','usuario','nombre','idEscuela','idUsuario',
			'idUser')
	def get_idEscuela(self,obj):
		return obj.idEscuela.pk
	def get_usuario(self,obj):
		userauth = UserAuth.objects.get(pk=obj.idUser)
		return userauth.username
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
		algo = re.match('\w{8}',value)
		if algo:
		   return value
		else:
			raise serializers.ValidationError("Password's length must be at least 8 characters")
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
class UsuarioUpdateSerializer(serializers.Serializer):
	contrasena = serializers.CharField(required=False)
	nombre = serializers.CharField(required=False)
	usuario = serializers.CharField(required=False)
	idUsuario = serializers.IntegerField(required=True)
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
	def update(self, validated_data):
		instance = Usuarios.objects.get(pk=self.data.get('idUsuario'))
		userauth = UserAuth.objects.get(pk=instance.idUser)
		try:
			userauth.set_password(self.data.get('contrasena'))
			userauth.save()
		except:
			None
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
	idEscuela = serializers.IntegerField(required=True)
	nombre = serializers.CharField(required=True)
	class Meta:
		model = Escuelas
		fields = ('nombre','idEscuela')
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
		
class idUsuarioSerializer(serializers.Serializer):
	#idUsuario = serializers.IntegerField(required=True)
	class Meta:
		model = Usuarios
		fields = ('idUsuario',)
class GrupoSerializer(serializers.Serializer):
	nombre = serializers.CharField(required=True)
	idUsuario = idUsuarioSerializer(many=True)
	class Meta:
		model = Grupos
		fields = ('nombre','idUsuario')


class GrupoCreateSerializer(serializers.Serializer):
	nombre = serializers.CharField(required=True)
	idUsuario = serializers.ListField(required=True)
	class Meta:
		model = Grupos
		fields = ('nombre','idUsuario')
	def create(self, validated_data):
		aux_IdUsuario = self.data.get('idUsuario')
		
		grupo = Grupos(nombre=self.data.get('nombre'))
		grupo.save()
		for x in aux_IdUsuario:
			grupo.idUsuario.add(x['idUsuario'])
		grupo.save()
		return GrupoSerializer(grupo).data

class LeccionSerializer(serializers.Serializer):
	idLeccion = serializers.CharField(required=False)
	nombre = serializers.CharField()
	class Meta:
		model = Leccion
		fields = ('nombre')
	def create(self,validated_data):
		return Leccion.objects.create(**validated_data)
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
class PuntuacionSerializer(serializers.Serializer):
	idPuntuacion = serializers.IntegerField(required=False)
	puntuacion = serializers.IntegerField()
	idUsuario = serializers.IntegerField()
	idLeccion = serializers.IntegerField()
	class Meta:
		model = Leccion
		fields = ('idPuntuacion','puntuacion','idUsuario','idLeccion')
	def create(self,validated_data):
		idUsuario_aux = Usuarios.objects.get(idUsuario=validated_data.pop('idUsuario'))
		idLeccion_aux = Leccion.objects.get(pk=validated_data.pop('idLeccion'))

		return PuntuacionAuxSerializer(Puntuaciones.objects.create(**validated_data,idUsuario=idUsuario_aux,
			idLeccion=idLeccion_aux)).data

	def update(self, instance, validated_data):
		instance.puntuacion = validated_data.get('puntuacion', instance.puntuacion)
		instance.save()
		return instance

