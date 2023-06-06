from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from plans.models import Plan

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id): #item_id is id of plan
    """ Add a number of sepcific plan to the shopping bag (note no plan is the same-tweaked and tailored) """
    plan = Plan.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity')) #get quantity from form and convert to integer-comes from template as string
    redirect_url = request.POST.get('redirect_url') #get redirect so we know where to redirect at end of process
    bag = request.session.get('bag', {}) #between view and form...session used to allow information to be stored until client and server finished communicating
    #store shopping items in session, persists until user closes browser so they can continuously add things to bag w/o losing contents
    #check if bag variable is there is it exists in session, if not initialise to empty dictionary
    if item_id in list(bag.keys()):
        bag[item_id] += quantity #if item is already in bag, increment quantity
    else:
        bag[item_id] = quantity
        messages.success(request,f'Added {plan.name} to your bag')
    #plan can be put in dictionary with quantity
    request.session['bag'] = bag #overwrite variable in session with updated version
    return redirect(redirect_url) 

def adjust_bag(request, item_id): #item_id is id of plan
    """ Adjust the quantity of the specified product to the specified amount """

    quantity = int(request.POST.get('quantity')) 
    bag = request.session.get('bag', {}) #no redirect url needed as always want to redirect to shopping bag page

    if quantity > 0:
        bag[item_id]
    else:
            del bag[item_id] 

    request.session['bag'] = bag 
    return redirect(reverse('view_bag')) 

def remove_from_bag(request, item_id): #item_id is id of plan
    """ Remove an item from the shopping bag, don't need quantity as quantity supposed to be zero """
    try:
        bag = request.session.get('bag', {}) #no redirect url needed as always want to redirect to shopping bag page

        if quantity > 0:
            bag[item_id]
        else:
                del bag[item_id] 

        request.session['bag'] = bag 
        return HttpResponse(status=200) #because view posted to fro a javascript function, return a 200 Http response (implying item successfully removed)
    
    except Exception as e:
        return HttpResponse(status=200)
