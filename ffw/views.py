from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    return render(request, 'ffw/index.html')

def privacy(request):
    """ A view to return the privacy page """
    return render(request, 'ffw/privacy.html')

def techniques(request):
    """ A view to return the techniques page """
    return render(request, 'ffw/techniques.html')
