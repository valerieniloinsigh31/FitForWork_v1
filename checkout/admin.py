from django.contrib import admin
from .models import OrderPlan, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderPlanAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,) 
    readonly_fields = ('order_number','date', 
                       'order_total', 'total',
                       'original_bag','stripe_pid',)

    fields = ('order_number', 'user_profile', 'date', 'full_name', 
                'email', 'phone_number', 'country',
                'eircode', 'town_or_city', 'street_address_1', 
                'street_address_2', 'county',
                'order_total', 'total',
                'original_bag','stripe_pid',)
        
    list_display = ('order_number', 'date', 'full_name', 
                    'order_total','total',)

    ordering = ('-date',)

admin.site.register(OrderPlan, OrderPlanAdmin)



