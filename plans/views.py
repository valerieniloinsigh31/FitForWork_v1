from django.shortcuts import render, get_object_or_404
from .models import Plan

def all_plans(request):
    """ A view to show all plans, including sorting and search queries """

    plans = Plan.objects.all()

    context = {
        'plans': plans,
    } #context added so that plans are available in the template...we can use this template variable in the html template

    return render(request, 'plans/plans.html', context) #We need to send things back to the template

def plan_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(Plan, pk=plan_id)

    context = {
        'plan': plan,
    } #add plan_id as parameter and consider singular plan as opposed to plans

    return render(request, 'plans/plan_detail.html', context) #We need to send things back to the template