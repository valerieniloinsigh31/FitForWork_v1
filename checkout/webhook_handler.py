from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request): #init method of class is a setup method called every time an instance of the class is created
        self.request = request #use it to assign the request as an attribute of the class in case we need to access any attributes of request coming from stripe

    def handle_event(self, event): #class method, takes event stripe sends and return http response indicating it was received
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)