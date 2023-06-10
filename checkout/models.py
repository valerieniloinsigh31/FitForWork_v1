import uuid #used to generate order number
from django.db import models
from django.db.models import Sum
from django.conf import settings

from plans.models import Plan #as line_item model has foreign key to Plan model

class OrderPlan(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False) #editable=False, we want generated order number to be unique and permanent so user's can find previous orders
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    eircode = models.CharField(max_length=15, null=True, blank=True) #not required as doesn't exist in every country
    town_or_city = models.CharField(max_length=25, null=False, blank=False)
    street_address_1 = models.CharField(max_length=100, null=False, blank=False)
    street_address_2 = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=60, null=True, blank=True) #not required as doesn't exist in every country
    date = models.DateField(auto_now_add=True) #automatically sets new order, date and time when new order created
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='') #if somebody wants to order the same thing twice
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='') #if somebody wants to order the same thing twice
#think about what we could add here...sport of consumer?

    def _generate_order_number(self):
        """
        Generate a random, unique order number, using UUID 
        """

        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        
        self.grand_total = self.order_total #no if statement involving delivery threshold
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey(OrderPlan, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')#when accessing orders, can make calls such as order.lineitems.all or order.lineitems.filter
    plan = models.ForeignKey(Plan, null=False, blank=False, on_delete=models.CASCADE) #ForeignKey to Plan so we can access all the fields in Plan model also
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    #think about what we could add here...sport of consumer?
    # basic idea is when user checks out first info used in payment form
    #to create order then iterate through items in shopping bag, create orderlineitem for each on and
    #attach to order and update otder_total and grand_total along way

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.plan.price * self.quantity
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Order {self.order.order_number}'