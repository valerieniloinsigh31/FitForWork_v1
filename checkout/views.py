from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderPlan, OrderLineItem
from plans.models import Plan
from bag.contexts import bag_contents #makes this available for use in our views

import stripe
import json #using to add  bag to metadata

@require_POST
def cache_checkout_data(request):  #to determine if user had save_info box checked...no way to determin in webhook whether user had checked...add in metadata key
    try:
        pid = request.POST.get('client_secret').split('_secret')[0] #first part of client_secret=payment intent id
        stripe.api_key = settings.STRIPE_SECRET_KEY #to modify payment intent
        stripe.PaymentIntent.modify(pid, metadata={     #modification is adding metadata
            'bag': json.dumps(request.session.get('bag', {})), #json dump of shopping bag to be used later
            'save_info': request.POST.get('save_info'), #whether user wants to save info
            'username': request.user, #user placing order
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400) #wrapped in a try except block-if anything goes wrong, error msg 

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'eircode': request.POST['eircode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address_1': request.POST['street_address_1'],
            'street_address_2': request.POST['street_address_2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid(): 
            order = order_form.save(commit=False) #prevent multiple save events with commit=False, prevent first one from happening
            pid = request.POST.get('client_secret').split('_secret')[0] #as per cache view
            order.stripe_pid = pid #so consumer can purchase same order twice
            order.original_bag = json.dumps(bag) #so consumer can purchase same order twice. dump to json string, set on order, save
            for item_id, item_data in bag.items():
                try:
                    plan = Plan.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                            order=order,
                            plan=plan,
                            quantity=item_data,
                        )
                    order_line_item.save()
    
                except Plan.DoesNotExist:
                    messages.error(request, (
                        "One of the plans in your bag wasn't found in our offering. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('plans'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()



    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """ 
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(OrderPlan, order_number=order_number)
    messages.success(request, f'Successfully ordered your tailored plan. \
        Your order number is {order_number}. A confirmation \
            email will be sent to {order.email} ')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context) 