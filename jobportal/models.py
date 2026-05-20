from django.db import models

# 1. Job Model: Isme Jobs ki details save hongi
class Job(models.Model):
    title = models.CharField(max_length=200) # Job ka naam
    company_name = models.CharField(max_length=200) # Company ka naam
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract')])
    description = models.TextField() # Job ki puri detail
    created_at = models.DateTimeField(auto_now_add=True) # Kab post hui

    def __str__(self):
        return self.title

# 2. Application Model: Isme Apply karne walo ka data save hoga
class Application(models.Model):
    # Yeh line application ko job se jodti hai
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/') # Resume file path
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.job.title if self.job else 'General'}"