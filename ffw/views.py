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

def founder(request):
    """ A view to return the founder page """
    return render(request, 'ffw/founder.html')

def tiers(request):
    """ A view to return the tiers page """
    return render(request, 'ffw/tiers.html')

def nutrition_newsletter(request):
    """ A view to return the nutrition_newsletter page """
    return render(request, 'ffw/nutrition_newsletter.html')
