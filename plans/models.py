from django.db import models

class Occupation(models.Model):
    name = models.CharField(max_length=350) #programmatic way to find in views.py and elsewhere
    friendly_name = models.CharField(max_length=350, null=True, blank=True) #nicer

    def __str__(self):
        return self.name #just returns products name

    def get_friendly_name(self):
        return self.friendly_name

class Plan(models.Model):
    occupation = models.ForeignKey('Occupation', null="True", blank="True", on_delete=models.SET_NULL)
    technique = models.ForeignKey('Technique', null="True", blank="True", on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    level = models.CharField(max_length=100,null=True, blank=True)
    goal = models.CharField(max_length=100, null=True, blank=True) #this has to be one of three options weight loss, muscle gain, get fit
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


#Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns products name


class Technique(models.Model):
    occupation = models.ForeignKey('Occupation', null="True", blank="True", on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    technique = models.TextField()
    
    #Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns products name