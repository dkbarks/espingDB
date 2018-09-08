from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UploadFileForm
from .forms import handle_uploaded_file



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()

    return render(request, 'home.html', {'form': form})