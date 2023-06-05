from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id): #item_id is id of plan
    """ Add a number of sepcific plan to the shopping bag (note no plan is the same-tweaked and tailored) """

    quantity = int(request.POST.get('quantity')) #get quantity from form and convert to integer-comes from template as string
    redirect_url = request.POST.get('redirect_url') #get redirect so we know where to redirect at end of process
    bag = request.session.get('bag', {}) #between view and form...session used to allow information to be stored until client and server finished communicating
    #store shopping items in session, persists until user closes browser so they can continuously add things to bag w/o losing contents
    #check if bag variable is there is it exists in session, if not initialise to empty dictionary
    if item_id in list(bag.keys()):
        bag[item_id] += quantity #if item is already in bag, increment quantity
    else:
        bag[item_id] = quantity
    #product can be put in dictionary with quantity
    request.session['bag'] = bag #overwrite variable in session with updated version
    return redirect(redirect_url) 