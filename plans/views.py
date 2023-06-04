from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.db.models import Q
from .models import Plan

def all_plans(request):
    """ A view to show all plans, including sorting and search queries """

    plans = Plan.objects.all()
    query = None
    #start with query as 'None' so we don't get error when loading plans page without search term

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('plans'))

                queries = Q(name_icontains=query) | Q(description_icontains=query)
                #use of pipe | allows OR logic...i makes queries case insensitive
                plans = plans.filter(queries)

    #Search action, text input named in form q, if q in request.get, set to query. 
    #if query is blank, no returned results, use django messages framework to attach error msg and redirect to plans url 
    #import messages, redirect, reverse, get_object_or_404
    #query not blank...object...use Q (special object from django.db.models) to generate search query
    #in django (produc.tobjects.filter) everything is anded together...for queries this means to match term needs to be in 
    #name and description...but we want either...accomplish OR logic, use Q-read through queries portion of Django docs
    
    context = {
        'plans': plans,
        'search_term': query, 
    } #context added so that plans are available in the template...we can use this template variable in the html template
    #added query to context
    return render(request, 'plans/plans.html', context) #We need to send things back to the template

def plan_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(Plan, pk=plan_id)

    context = {
        'plan': plan,
    } #add plan_id as parameter and consider singular plan as opposed to plans

    return render(request, 'plans/plan_detail.html', context) #We need to send things back to the template