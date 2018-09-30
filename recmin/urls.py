# -*- coding: utf-8 -*-
"""
Created on Sun Sep 9 05:39:38 2018

@author: David Cabarcas
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^index/', views.index, name="index"),
    url(r'^upload/', views.upload, name="upload"),
    url(r'^minimun/', views.minimun, name="minimun"),
]