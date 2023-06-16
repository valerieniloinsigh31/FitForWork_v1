from django import forms
from .widgets import CustomClearableFileInput
from .models import Plan, Technique


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = '__all__'

    image = forms.ImageField(label="Image", required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        techniques = Technique.objects.all()
        friendly_names = [(t.id, t.get_friendly_name()) for t in techniques] 

        self.fields['technique'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0' 
            