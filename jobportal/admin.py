from django.contrib import admin
from .models import Job, Application, HireTalent

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type') 
    search_fields = ('title', 'company_name') 

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'applied_at')

@admin.register(HireTalent)
class HireTalentAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'industry',
        'email',
        'role',
        'created_at'
    )
    search_fields = (
        'company_name',
        'role',
        'email'
    )