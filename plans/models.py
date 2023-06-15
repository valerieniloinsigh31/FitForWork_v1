from django.db import models

class Plan(models.Model):
    technique = models.ForeignKey('Technique', null="True", blank="True", on_delete=models.SET_NULL)
    jobtype = models.ForeignKey('JobType', null="True", blank="True", on_delete=models.SET_NULL)
    goal = models.ForeignKey('Goal', null="True", blank="True", on_delete=models.SET_NULL)
    tier = models.ForeignKey('Tier',null="True", blank="True", on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


#Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of plan

class Technique(models.Model):
    name = models.CharField(max_length=300)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    technique = models.TextField()
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    #Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of technique

    def get_friendly_name(self):
        return self.friendly_name

class JobType(models.Model):
    name = models.CharField(max_length=300)
    jobtype = models.TextField()

#Not blank=true, null=true, each plan requires a name, description, price, everything else is optional
    def __str__(self):
        return self.name #just returns name of type


#Consider adding a model for Goal and a model for level
#Consider nutrition newsletter and supplementary info on supplements

class Goal(models.Model):
    name = models.CharField(max_length=500)
    goal = models.TextField()

    def __str__(self):
        return self.name


class Tier(models.Model):
    name = models.CharField(max_length=200)
    tier = models.IntegerField()  


    def __str__(self):
        return self.name
