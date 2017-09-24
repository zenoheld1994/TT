#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
class Escuelas(models.Model):
	class Meta:
		db_table = "Escuelas"
	idEscuela = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50,blank=False,unique=True)
class Leccion(models.Model):
	class Meta:
		db_table = "Leccion"
	idLeccion = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50,unique=True)
class Grupos(models.Model):
	class Meta:
		db_table = "Grupos"
	idGrupo = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=30,blank=False,unique=False)
class Usuarios(models.Model):
	class Meta:
		db_table = "Usuarios"
	idUsuario = models.AutoField(primary_key=True)
	tipoUsuario = models.BooleanField(blank=False)
	nombre = models.CharField(max_length=100,blank=False)
	idUser = models.IntegerField(blank=False,unique=True)
	idEscuela = models.ForeignKey(Escuelas, on_delete=models.CASCADE,db_column='idEscuela')
	idGrupo = models.ForeignKey(Grupos,on_delete=models.SET_NULL,null=True,db_column='idGrupo')
class Puntuaciones(models.Model):
	class Meta:
		db_table = "Puntuaciones"
	idPuntuacion = models.AutoField(primary_key=True)
	puntuacion = models.IntegerField(blank=True)
	idUsuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE,blank=False,db_column='idUsuario')
	idLeccion = models.ForeignKey(Leccion, on_delete=models.CASCADE,blank=False,db_column='idLeccion')


	





