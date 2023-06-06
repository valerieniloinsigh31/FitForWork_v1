from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        import checkout.signals #Lets Django know there's a new signals module with
        #listeners in it. This is here to over-ride the ready method and import signals module
        #Every time a lineitem is saved or deleted, custom total update total model method will be called, updating order totals