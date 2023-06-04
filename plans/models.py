from django.db import models

class Occupation(models.Model):
    name = models.CharField(max_length=350) #programmatic way to find in views.py and elsewhere
    friendly_name = models.CharField(max_length=350, null=True, blank=True) #nicer

    def __str__(self):
        return self.name #just returns name of occupation

    def get_friendly_name(self):
        return self.friendly_name

class Plan(models.Model):
    occupation = models.ForeignKey('Occupation', null="True", blank="True", on_delete=models.SET_NULL)
    technique = models.ForeignKey('Technique', null="True", blank="True", on_delete=models.SET_NULL)
    type = models.ForeignKey('Type', null="True", blank="True", on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    level = models.CharField(max_length=100,null=True, blank=True)
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


#Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of plan


class Technique(models.Model):
    name = models.CharField(max_length=300)
    technique = models.TextField()
    
    #Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of technique

class Type(models.Model):
    name = models.CharField(max_length=300)
    type = models.TextField()
    
    #Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of type

#Consider adding a model for Goal and a model for level
#Consider nutrition newsletter and supplementary info on supplements