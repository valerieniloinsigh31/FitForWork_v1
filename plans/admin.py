from django.contrib import admin
from .models import Plan, Technique, JobType, Goal, Tier 

class PlanAdmin(admin.ModelAdmin):
    list_display = ( 
    'name',
    'technique',
    'jobtype',
    'price',
    'image',
    'goal',
    'tier'
    )

    ordering = ('price',) 

class TechniqueAdmin(admin.ModelAdmin):
    list_display = ( 
    'name',
    'technique',
    'image',
    )

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ( 
    'name',
    'jobtype',
    )

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

