from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save #in order for signal to work 
from django.dispatch import receiver #in order for signal to work 

from django_countries.fields import CountryField


class UserProfile(models.Model): #one to one field attached to User
    """
    A user profile model for maintaining default
    order history - no delivery
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one field attached to User each user only one profile, each profile attached to one user
    default_phone_number = models.CharField(max_length=20, null=True, blank=True) # for delivery optional here so null and blank=True
    default_country = CountryField(blank_label='Country *', null=True, blank=True) # for delivery optional here so null and blank=True
    default_eircode = models.CharField(max_length=20, null=True, blank=True) # for delivery optional here so null and blank=True
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True) # for delivery optional here so null and blank=True
    default_street_address_1 = models.CharField(max_length=80, null=True, blank=True) # for delivery optional here so null and blank=True
    default_street_address_2 = models.CharField(max_length=80, null=True, blank=True) # for delivery optional here so null and blank=True
    default_county = models.CharField(max_length=80, null=True, blank=True) # for delivery optional here so null and blank=True

    def __str__(self):
        return self.user.username #to return username

#only one signal for in this models subfolder so no need for separate signals file
@receiver(post_save, sender=User) #each time user object saved, profile created or update existing profile
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()