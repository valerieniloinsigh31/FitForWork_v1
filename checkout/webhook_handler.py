from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import OrderPlan, OrderLineItem
from plans.models import Plan
from profiles.models import UserProfile

import json
import time
import stripe

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request): 
        self.request = request 

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )     


    def handle_event(self, event): 
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent_succeeded webhook event from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info


        stripe_charge = stripe.Charge.retrieve(
        intent.latest_charge
)

        billing_details = stripe_charge.billing_details 
        #shipping_details = intent.shipping
        total = round(stripe_charge.amount / 100, 2) 

        
        #for field, value in billing_details.address.items(): 
        #    if value == "":
        #        billing_details.address[field] = None

       
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = billing_details.phone
                profile.default_country = billing_details.address.country
                profile.default_eircode = billing_details.address.eircode
                profile.default_town_or_city = billing_details.address.city
                profile.default_street_address_1 = billing_details.address.line1
                profile.default_street_address_2 = billing_details.address.line2
                profile.default_county = billing_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = OrderPlan.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    eircode__iexact=billing_details.address.eircode,
                    town_or_city__iexact=billing_details.address.city,
                    street_address_1__iexact=billing_details.address.line1,
                    street_address_2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    total=total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except OrderPlan.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = OrderPlan.objects.create(
                    full_name=billing_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    eircode=billing_details.address.eircode,
                    town_or_city=billing_details.address.city,
                    street_address_1=billing_details.address.line1,
                    street_address_2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items(): 
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
        self._send_confirmation_email(order)
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