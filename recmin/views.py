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
from taller3 import calculaLlaves
# Create your views here.
def home(request):
    return render(request, 'home.html', {'what':'ESPECIALIZACION INGENIERIA DE SOFTWARE', 'db':'BASES DE DATOS'})

def index(request):
    return render(request, 'index.html', {'what':'RECUBRIMIENTO MINIMO Y LLAVES CANDIDATAS'})

def upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        data = manage_uploaded(str(request.FILES['file']))
        atributos = str(data["T"]).replace('u','')
        dependencias = str(data["L"]).replace('u','')
        return render(request, 'editar.html', {'atributos': atributos,'dependencias':dependencias})
    else:
        return render(request, 'editar.html', {'atributos': '','dependencias':''})

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
        llave = calculaLlaves(a,d)
        generar_json('* Informe primer paso:'+str(result[3])+'* Primer paso: '+str(result[0])+'* Informe segundo paso:'+str(result[4])+'* Segundo paso: '+str(result[1])+'* Informe tercer paso:'+str(result[0])+'* Tercer paso:'+str(result[2]))
        generar_json_llaves('Z :'+str(llave[2])+'Z+ :'+str(llave[3])+'W :'+str(llave[4])+'V :'+str(llave[5]))
        return render(request, 'resultados.html', {'info1': result[2],'info2': llave[0],'info3': llave[1]})

def generar_json(data):
    filePathNameWExt = 'up\cierre.csv'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(data)
        fp.close()

def generar_json_llaves(data):
    filePathNameWExt = 'up\llaves.csv'
    with open(filePathNameWExt, 'w') as fp:
        fp.write(data)
        fp.close()