# -*- coding: utf-8 -*-
"""
Created on Sun Sep 9 05:45:01 2018

@author: David Cabarcas
"""
from django import forms

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    archivo = forms.FileField()
    
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
class FinalForm(forms.Form):
    atrib = forms.CharField()
    dep = forms.CharField()