from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Plan, Technique, JobType, Occupation
from .forms import PlanForm

def all_plans(request):
    """ A view to show all plans, including sorting and search queries """

    plans = Plan.objects.all()
    query = None
    #start with query as 'None' so we don't get error when loading plans page without search term
    techniques = None
    jobtypes = None
    sort = None
    direction = None
    occupations = None
    
    #N.B. direction for filtering level is alphabetical (Advanced/Beginner/Intermediate-not ideal. Would be better as 
    # Beginner/Intermediate/Advanced...how to do this-ordering?)
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                plans = plans.annotate(lower_name =Lower('name'))
#add conditional, if the sort-key is equal to occupation, adjust to tack on __name , to sort occupations by name, not ids. __ allows 
# us to drill into a related model...changing to plans.order_by occupation__name:
            if sortkey == 'occupation':
                sortkey = 'occupation__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f-{sortkey}
            #if descending, add minus in front of sortkey with string formatting, which reverses order...need to alter for goals, can't be alphabetical
            plans = plans.order_by(sortkey)

        if 'occupation' in request.GET:
            occupations = request.GET['occupation'].split(',')
            plans = plans.filter(occupation__name__in=occupations)
            occupations =  Occupation.objects.filter(name__in=occupations) 
        
        #Occupation added-more filtering functionality

        if 'technique' in request.GET:
            techniques = request.GET['technique'].split(',')
            plans = plans.filter(technique__name__in=techniques)
            techniques = Technique.objects.filter(name__in=techniques)

        #techniques filtered down to list of ones whose name are in the url...converting list of techniques strings into list of technique objects
        #as we can access fields in template for objects...must return to context to use in template later on
        #can do this because plans and techniques are related with a foreign key
        #__ syntax allows us to drill into related model - models related by a foreign key

        if 'jobtype' in request.GET:
            jobtypes = request.GET['jobtype'].split(',')
            plans = plans.filter(jobtype__name__in=jobtypes)
            jobtypes = JobType.objects.filter(name__in=jobtypes)

         #JobType and Plan models related by a ForeignKey so should be able to filter...  

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('plans'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            #use of pipe | allows OR logic...i makes queries case insensitive
            plans = plans.filter(queries)


    #Search action, text input named in form q, if q in request.get, set to query. 
    #if query is blank, no returned results, use django messages framework to attach error msg and redirect to plans url 
    #import messages, redirect, reverse, get_object_or_404
    #query not blank...object...use Q (special object from django.db.models) to generate search query
    #in django (product.objects.filter) everything is anded together...for queries this means to match term needs to be in 
    #name and description...but we want either...accomplish OR logic, use Q-read through queries portion of Django docs
    

    current_sorting = f'{sort}_{direction}'
    #return sorting methodology to template...using string both sort and direction variable stored-easy to do with string formatting

    context = {
        'plans': plans,
        'search_term': query, 
     #context added so that plans are available in the template...we can use this template variable in the html template
    #added query to context
        'current_techniques': techniques,
        'current_jobtypes': jobtypes,
        'current_sorting': current_sorting,
        'current_occupations': occupations,
        }
        #list of technique objects-returned to context so we can use in template later on
    return render(request, 'plans/plans.html', context) #We need to send things back to the template

def plan_detail(request, plan_id):
    """ A view to show individual plan details """
    print('plan_id: ', plan_id)
    plan = get_object_or_404(Plan, pk=plan_id)

    context = {
        'plan': plan,
    } #add plan_id as parameter and consider singular plan as opposed to plans

    return render(request, 'plans/plan_detail.html', context) #We need to send things back to the template

def add_plan(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save()
            messages.success(request, 'Successfully added plan!')
            return redirect(reverse('plan_detail', args=[plan.id]))
        else:
            messages.error(request, 'Failed to add plan. Please ensure the form is valid.')
    else:
        form = PlanForm()
        
    template = 'plans/add_plan.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_plan(request, product_id):
    """ Edit a plan on the website """
    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated plan!')
            return redirect(reverse('plan_detail', args=[plan.id]))
        else:
            messages.error(request, 'Failed to update plan. Please ensure the form is valid.')
    else:
        form = PlanForm(instance=plan)
        messages.info(request, f'You are editing {plan.name}')

    template = 'plans/edit_plan.html'
    context = {
        'form': form,
        'plan': plan,
    }

    return render(request, template, context)

def delete_plan(request, plan_id):
    """ Delete a plan from the store """
    plan = get_object_or_404(Plan, pk=plan_id)
    plan.delete()
    messages.success(request, 'Plan deleted!')
    return redirect(reverse('plans'))