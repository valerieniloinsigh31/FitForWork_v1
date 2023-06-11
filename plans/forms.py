from django import forms
from .models import Plan, Technique


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        techniques = Technique.objects.all()
        friendly_names = [(t.id, t.get_friendly_name()) for t in techniques] #list comprehension

        self.fields['technique'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0' #will be seen in selext box generated in form