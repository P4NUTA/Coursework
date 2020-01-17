"""Coursework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    re_path('^404', views.error404),
    path(r'user', views.userrender),
    path(r'moderator', views.moderatorrender),
    path(r'admin', views.adminrender),
    path(r'moderatorlist', views.moderatorlist),
    path(r'userlist', views.userlist),
    re_path(r'^portlist/(?P<dock>\w+)/(?P<port>)/$', views.shiplist),
    re_path(r'^portlist/(?P<dock>\w+)/$', views.docklist),
    path(r'portlist/<str:id>', views.portlist),
    path(r'portlist', views.portlist),
]
