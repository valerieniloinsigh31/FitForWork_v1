from django.contrib import admin
from .models import Plan, Technique, JobType, Goal, Tier 

class PlanAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'name',
    'technique',
    'jobtype',
    'price',
    'image',
    'goal',
    'tier'
    )

    ordering = ('tier',) #since it has to order on multiple columns, has to be a tuple even though it's only one field

#extends the builtin ModelAdmin class
#to change the order of columns in admin, adjust order here in list_display attribute

#extends the builtin ModelAdmin class
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'name',
    'technique',
    )
#extends the builtin ModelAdmin class

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ( #attribute that is a tuple that will tell the admin which fields to display
    'name',
    'jobtype',
    )
#extends the builtin ModelAdmin class

class GoalAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'goal',
    )

class TierAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tier',
    )


admin.site.register(Plan)
admin.site.register(Technique)
admin.site.register(JobType)
admin.site.register(Goal)
admin.site.register(Tier)

