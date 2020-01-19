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
    path(r'user', views.userrender, name = "menuuser"),
    path(r'moderator', views.moderatorrender, name="menumoderator"),
    path(r'admin', views.adminrender, name="menuadmin"),
    path(r'moderatorlist', views.moderatorlist, name="moderatorlist"),
    path(r'userlist', views.userlist, name="userlist"),
    # re_path(r'^portlist/(?P<dock>\w+)/(?P<port>)/$', views.shiplist),
    # re_path(r'^portlist/(?P<id>\w+)/$', views.portinfo, name="portinfo"),
    path(r'portlist', views.portlist, name="portlist"),
    path(r'portlist/<int:id>/', views.portinfo, name="portinfo"),
    path(r'portlist/<int:id>/<int:dock>/', views.dockinfo, name="dockinfo"),
    path(r'adduser', views.adduser, name="adduser"),
    path(r'addmoderator', views.addmoderator, name="addmoderator"),
    path(r'addport', views.addport, name="addport"),
    path(r'portlist/<int:id>/adddock', views.adddock, name="adddock"),
path(r'portlist/<int:id>/addworker', views.addworker, name="addworker"),
    path(r'logout', views.logout, name="logout"),
    # path(r'portlist/<int:id>/<int:worker>', views.portinfo, name="workerlist"),
]
