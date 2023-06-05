from decimal import Decimal 
from django.conf import settings 

def bag_contents(request):

    bag_items = []
    total = 0 #intialise to 0
    plan_count = 0 #intialise to 0

    if total < settings.FREE_PT_THRESHOLD:

        free_pt_delta = settings.FREE_PT_THRESHOLD - total #Allows user to know how much more they have to spend to get a free consultation
    else:
        print ("No free PT session for you!")

    context = {
        'bag_items':bag_items,
        'total': total,
        'plan_count': plan_count,
        'free_pt_delta': free_pt_delta,
        'free_pt_threshold': settings.FREE_PT_THRESHOLD,
        'grand_total': grand_total,
        
    } #function returns dictionary called 'context'...add items to context so available in templates across the site

    return context #this is a context processor. It's purpose is to make this dictionary available to all templates across
    #the application. Like use of 'request.user' across templates due to built-in request context-processor. to 
    #To make available to all apps, needs to be added tp list of 'context-processors' in templates variable in project
    #level settings.py file