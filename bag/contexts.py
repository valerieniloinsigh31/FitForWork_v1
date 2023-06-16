from decimal import Decimal 
from django.conf import settings 
from django.shortcuts import get_object_or_404
from plans.models import Plan


def bag_contents(request):

    bag_items = []
    total = 0 
    plan_count = 0 
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

    total = total 

    context = {
        'bag_items':bag_items,
        'total': total,
        'plan_count': plan_count,
    } 

    return context 