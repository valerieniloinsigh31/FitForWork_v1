from django import forms
from .models import OrderPlan


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderPlan
        fields = ('full_name', 'email', 'phone_number',
                  'street_address_1', 'street_address_2',
                  'town_or_city', 'eircode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs): #over-riding init method which allows customization
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field...what is autofocus
        """
        super().__init__(*args, **kwargs) #call default init method, to set form up as it would be, by default
        placeholders = {   #dictionary of placeholders that show in form fields rather than clunky labels and textboxes                  
            'full_name': 'What is your Name?',
            'email': 'Give us your email address...',
            'phone_number': 'Can I get your number?',
            'country': 'Country',
            'eircode': 'Eircode',
            'town_or_city': 'Town or City',
            'street_address_1': 'Street Address 1',
            'street_address_2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True #set autofocus attribute on full_name field-this makes cursor start in full_name field
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False #iterate through forms fields, adding star to placeholder if required field on model and
            #setting placeholder values to their values in the dictionary above and
            #adding a CSS class we will use later (stripe-style-input)
            #removing form fields labels since we won't need them once placeholders are set