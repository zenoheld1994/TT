#-*- coding: utf-8 -*-
"""TT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from django.conf.urls import include
from Usuarios import api as apiUsuarios
router = routers.SimpleRouter()
router.trailing_slash = '/?'
router.register(r'v1/usuarios',apiUsuarios.UsuariosViewSet,base_name='usuario')
router.register(r'v1/escuelas',apiUsuarios.EscuelasViewSet,base_name='escuela')
router.register(r'v1/grupos',apiUsuarios.GruposViewSet,base_name='grupo')
router.register(r'v1/lecciones',apiUsuarios.LeccionViewSet,base_name='leccion')
router.register(r'v1/puntuaciones',apiUsuarios.PuntuacionViewSet,base_name='puntuacion')
router.register(r'v1/everyone',apiUsuarios.EveryoneViewSet,base_name='everyone')



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'', include('Usuarios.urls')),
    
]


urlpatterns += router.urls