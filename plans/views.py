from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Plan, JobType, Technique
from .forms import PlanForm

def all_plans(request):
    """ A view to show all plans, including sorting and search queries """

    plans = Plan.objects.all()
    query = None
    jobtypes = None
    techniques = None
    sort = None
    direction = None
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                plans = plans.annotate(lower_name=Lower('name'))
            if sortkey == 'technique':
                sortkey = 'technique__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            plans = plans.order_by(sortkey)
            
        if 'technique' in request.GET:
            techniques = request.GET['technique'].split(',')
            plans = plans.filter(technique__name__in=techniques)
            techniques = Technique.objects.filter(name__in=techniques)
 
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('plans'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            plans = plans.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'plans': plans,
        'search_term': query, 
        #'current_jobtypes': jobtypes,
        'current_techniques': techniques,
        'current_sorting': current_sorting,
        }
    
    return render(request, 'plans/plans.html', context) 

def plan_detail(request, plan_id):
    """ A view to show individual plan details """
    plan = get_object_or_404(Plan, pk=plan_id)

    context = {
        'plan': plan,
    } 

    return render(request, 'plans/plan_detail.html', context) 

@login_required
def add_plan(request):
    """ Add a plan to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only website admin can do that.')
        return redirect(reverse('ffw'))

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

@login_required
def edit_plan(request, plan_id):
    """ Edit a plan on the website """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only website admin can do that.')
        return redirect(reverse('ffw'))

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

@login_required
def delete_plan(request, plan_id):
    """ Delete a plan from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only the website admin can do that.')
        return redirect(reverse('ffw'))
    plan = get_object_or_404(Plan, pk=plan_id)
    plan.delete()
    messages.success(request, 'Plan deleted!')
    return redirect(reverse('plans'))