from django.http import HttpResponse

from .models import OrderPlan, OrderLineItem
from plans.models import Plan

import json
import time

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request): #init method of class is a setup method called every time an instance of the class is created
        self.request = request #use it to assign the request as an attribute of the class in case we need to access any attributes of request coming from stripe

    def handle_event(self, event): #class method, takes event stripe sends and return http response indicating it was received
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)


    #for each type of webhook we want a method to handle it, makes them easier to manage
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent_succeeded webhook event from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

# Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
        intent.latest_charge
)

        billing_details = stripe_charge.billing_details # updated
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2) # updated

        #Clean data in the shipping details
        for field, value in shipping_details.address.items(): #ensure data in same form as what we want in database. replace empty strings with none
            if value == "":
                shipping_details.address[field] = None

        #Check if order exists. Start by assuming order exists   
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get( #iexact lookup field is exact match but case insensitive
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    eircode__iexact=shipping_details.address.eircode,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address_1__iexact=shipping_details.address.line1,
                    street_address_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break #because in while loop, if order is found, should break out of loop
            except Order.DoesNotExist:
                attempt += 1 #If order not found in db...create delay
                time.sleep(1)
        if order_exists: #outside loop
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    eircode=shipping_details.address.eircode,
                    town_or_city=shipping_details.address.city,
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag, #so consumer can purchase same order twice-if we don't find order in database, safe to create here
                    stripe_pid=pid,   #so consumer can purchase same order twice-if we don't find order in database, safe to create here
                )
                #for item_id, item_data in json.loads(bag).items(): #to be checked as a lot of size related code removed
                plan = Plan.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                              order=order,
                              plan=plan,
                              quantity=item_data,
                          )
                order_line_item.save()
            except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent_payment_failed webhook event from Stripe
        """
        return HttpResponse(
            content=f'Payment Failed Webhook received: {event["type"]}',
            status=200)


   
