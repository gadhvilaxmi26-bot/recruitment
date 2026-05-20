from django.contrib import admin
from .models import Job, Application

# Jobs ko admin mein dikhane ke liye
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type') # Columns jo bahar dikhengi
    search_fields = ('title', 'company_name') # Search bar enable karega

# Applications (Resumes) ko admin mein dikhane ke liye
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'applied_at')