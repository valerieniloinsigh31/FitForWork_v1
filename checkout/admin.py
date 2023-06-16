from django.contrib import admin
from .models import OrderPlan, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

    # allows us to add and edit line items in admin from inside OrderPlan model so
    # when we look at order, we will see a list of editable items on the same page
    #won't need to go to orderplan lineitem interface

class OrderPlanAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,) #to enable inline model
    readonly_fields = ('order_number','date', 
                       'order_total', 
                       'original_bag','stripe_pid',)

    fields = ('order_number', 'user_profile', 'date', 'full_name', 
                'email', 'phone_number', 'country',
                'eircode', 'town_or_city', 'street_address_1', 
                'street_address_2', 'county',
                'order_total', 
                'original_bag','stripe_pid',)
        
    list_display = ('order_number', 'date', 'full_name', 
                    'order_total',)

    ordering = ('-date',)

admin.site.register(OrderPlan, OrderPlanAdmin)
#no need to register OrderLineItem model class as accessible via the inline on the OrderPlan model


