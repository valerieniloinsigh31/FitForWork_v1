from django.shortcuts import render
from .models import Plan

# Create your views here.

def all_plans(request):
    """ A view to show all plans, including sorting and search queries """

    plans = Plan.objects.all()

    context = {
        'plans': plans,
    } #context added so that plans are available in the template...we can use this template vairbale in the html template

    return render(request, 'plans/plans.html', context) #Yet to build template for plans, needs a context as we need to send
    #things back to the template