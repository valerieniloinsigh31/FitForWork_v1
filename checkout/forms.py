from django import forms
from .models import OrderPlan


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderPlan
        fields = ('full_name', 'email', 'phone_number',
                  'street_address_1', 'street_address_2',
                  'town_or_city', 'eircode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field...what is autofocus
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'What is your Name?',
            'email': 'Give us your email address...',
            'phone_number': 'Can I get your number?',
            'eircode': 'Eircode',
            'town_or_city': 'Town or City',
            'street_address_1': 'Street Address 1',
            'street_address_2': 'Street Address 2',
            'county': 'County, State, Locality or Cell Number',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
            self.fields[field].label = False