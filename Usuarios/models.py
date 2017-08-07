from django.db import models
class Escuelas(models.Model):
	class Meta:
		db_table = "Escuelas"
	idEscuela = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50,blank=False)

class Leccion(models.Model):
	class Meta:
		db_table = "Leccion"
	idLeccion = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
class Usuarios(models.Model):
	class Meta:
		db_table = "Usuarios"
	idUsuario = models.AutoField(primary_key=True)
	tipoUsuario = models.BooleanField(blank=False)
	nombre = models.CharField(max_length=100,blank=False)
	idUser = models.IntegerField(blank=False)
	idEscuela = models.ForeignKey(Escuelas, on_delete=models.CASCADE)
class Puntuaciones(models.Model):
	class Meta:
		db_table = "Puntuaciones"
	idPuntuacion = models.AutoField(primary_key=True)
	puntuacion = models.IntegerField(blank=True)
	idUsuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE,blank=False)
	idLeccion = models.ForeignKey(Leccion, on_delete=models.CASCADE,blank=False)

class Grupos(models.Model):
	class Meta:
		db_table = "Grupos"
	idGrupo = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=30,blank=False,unique=True)
	idUsuario = models.ManyToManyField(Usuarios)





