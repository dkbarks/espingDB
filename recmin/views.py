# -*- coding: utf-8 -*-
"""
Created on Sun Sep 9 05:39:38 2018

@author: David Cabarcas
"""
from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from taller2 import cargar_datos
# Create your views here.
def home(request):
    return render(request, 'index.html', {'what':'RECUBRIMIENTO MINIMO'})

def upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        data = manage_uploaded(str(request.FILES['file']))
        atributos = str(data["T"]).replace('u','')
        dependencias = str(data["L"]).replace('u','')
        return render(request, 'editar.html', {'atributos': atributos,'dependencias':dependencias})

    return HttpResponse("Failed")

def handle_uploaded_file(file, filename):
    if not os.path.exists('up/'):
        os.mkdir('up/')

    with open('up/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def manage_uploaded(filename):
    filename = os.path.join('up/'+filename)
    with open(filename) as file:
        resf = json.load(file)
    return resf

def minimun(request):
    if request.method == 'POST':
        x = request.POST
        a=str(x['atrib']).replace('u','').strip()
        d=str(x['dep']).replace('u','').strip()
        result = cargar_datos(a,d)
        generar_json('* Recubrimiento Minimo: '+str(result[2]))
        return render(request, 'resultados.html', {'info1': result[3],'info2': result[4],'info3': result[5]})

def generar_json(data):
    filePathNameWExt = 'up\cierre.json'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(data)
        fp.close()
