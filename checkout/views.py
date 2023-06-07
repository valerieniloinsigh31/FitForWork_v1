from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request,"There are no plans in your bag at the mo!")
        return redirect(reverse('plans'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_live_mN9tBqmPsjW1nWTyQFSnhxgb', #stripe public key added
        'client_secret': 'test client secret', #test stripe secret key
    }

    return render(request, template, context)
