from decimal import Decimal 
from django.conf import settings 
from django.shortcuts import get_object_or_404
from plans.models import Plan


def bag_contents(request):

    bag_items = []
    total = 0 #initialise to 0
    plan_count = 0 #initialise to 0
    bag = request.session.get('bag', {}) #same as in add_to_bag view. Gets bag in session if exists, initializing to empty dictionary if not

    #in order to populate values of variables we are not using yet, we need to iterate through all of the items in 
    #the bag and along the way tally up total cost and plan count and add
    #plans and data to bag_items list to display throughout site and on bag page

    for item_id, quantity in bag.items():
        plan = get_object_or_404(Plan, pk=item_id) #first get plan
        total += quantity * plan.price #add qty*price to total
        plan_count += quantity #increment plan count by quantity
        bag_items.append({           #add dictionary to list of bag items containing id, quantity and plan object itself (gives us access to image etc)
            'item_id': item_id,
            'quantity': quantity,
            'plan': plan,       #add plan object itself so we have access to all of the other fields when iterating through bag items
        })


    #if total < settings.FREE_PT_THRESHOLD:

        #free_pt_delta = settings.FREE_PT_THRESHOLD - total #Allows user to know how much more they have to spend to get a free consultation
    #else:
        #print ("No free PT session for you!")

    grand_total = total #need to declare grand_total variable, updates bag total as seen in base.html code

    context = {
        'bag_items':bag_items,
        'total': total,
        'plan_count': plan_count,
        #'free_pt_delta': free_pt_delta,
        'free_pt_threshold': settings.FREE_PT_THRESHOLD,
        'grand_total': grand_total,
    } #function returns dictionary called 'context'...add items to context so available in templates across the site

    return context #this is a context processor. It's purpose is to make this dictionary available to all templates across
    #the application. Like use of 'request.user' across templates due to built-in request context-processor. to 
    #To make available to all apps, needs to be added tp list of 'context-processors' in templates variable in project
    #level settings.py file