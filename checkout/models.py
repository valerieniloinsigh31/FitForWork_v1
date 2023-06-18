import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField
from profiles.models import UserProfile

from plans.models import Plan


class OrderPlan(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    eircode = models.CharField(max_length=15, null=True, blank=True)
    town_or_city = models.CharField(max_length=25, null=False, blank=False)
    street_address_1 = models.CharField(max_length=100, null=False,
                                        blank=False)
    street_address_2 = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=60, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False,
                                  blank=False, default='')

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
    order = models.ForeignKey(OrderPlan, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    plan = models.ForeignKey(Plan, null=False, blank=False,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6,
                                         decimal_places=2, null=False,
                                         blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.plan.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.order.order_number}'
