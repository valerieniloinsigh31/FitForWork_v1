from decimal import Decimal 
from django.conf import settings 
from django.shortcuts import get_object_or_404
from plans.models import Plan


def bag_contents(request):

    bag_items = []
    total = 0 #initialise to 0
    plan_count = 0 #initialise to 0
    bag = request.session.get('bag', {}) 

    for item_id, item_data in bag.items():
        plan = get_object_or_404(Plan, pk=item_id)
        total += item_data * plan.price
        plan_count += item_data
        bag_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'plan': plan,
         })

    grand_total = total #need to declare grand_total variable, updates bag total as seen in base.html code

    context = {
        'bag_items':bag_items,
        'total': total,
        'plan_count': plan_count,
        'grand_total': grand_total,
    } #function returns dictionary called 'context'...add items to context so available in templates across the site

    return context #this is a context processor. It's purpose is to make this dictionary available to all templates across
    #the application. Like use of 'request.user' across templates due to built-in request context-processor. to 
    #To make available to all apps, needs to be added tp list of 'context-processors' in templates variable in project
    #level settings.py file