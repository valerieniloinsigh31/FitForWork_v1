from django.db.models.signals import post_save, post_delete #post in this case means after...django sends signals to app after model instance saved and deleted
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs): #function handles signals from post_save event, parameters
    #refer to sender of the signal (OrderLineItem), instance of model that sent it, a boolean sent by Django referring to whether
    #  it's a new instance or one being updated and any key word args
    """
    Update order total on lineitem update/create
    """

    instance.order.update_total() #access instance order lineitem is related to and call update_total method

  
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs): #function handles signals from post_save event, parameters
    #refer to sender of the signal (OrderLineItem), instance of model that sent it, a boolean sent by Django referring to whether
    #  it's a new instance or one being updated and any key word args
    """
    Update order total on lineitem delete
    """

    instance.order.update_total() #access instance order lineitem is related to and call update_total method

  