from django.contrib import admin
from .models import Plan, Occupation, Technique, Type

# Register your models here.

class PlanAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'name',
    'occupation',
    'technique',
    'type',
    'goal',
    'price',
    'level',
    'image',
    )

    ordering = ('level',) #since it has to order on multiple columns, has to be a tuple even though it's only one field

#extends the builtin ModelAdmin class
class OccupationAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'friendly_name',
    'name',
    )

#extends the builtin ModelAdmin class
#to change the order of columns in admin, adjust order here in list_display attribute

#extends the builtin ModelAdmin class
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'friendly_name',
    'name',
    'technique',
    )
#extends the builtin ModelAdmin class

class TypeAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'friendly_name',
    'name',
    'type',
    )
#extends the builtin ModelAdmin class


admin.site.register(Plan)
admin.site.register(Occupation)
admin.site.register(Technique)
admin.site.register(Type)
