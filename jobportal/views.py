from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  # ✅ Import missing for messages

from .models import Job, Application

# 1. Home View
def home_view(request):
    query = request.GET.get('search')
    if query:
        recent_jobs = Job.objects.filter(title__icontains=query).order_by('-created_at')[:6]
    else:
        recent_jobs = Job.objects.all().order_by('-created_at')[:6]
    return render(request, 'jobportal/index.html', {'recent_jobs': recent_jobs})

# 2. Jobs List
def jobs_view(request):
    all_jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobportal/jobs.html', {'jobs': all_jobs})

# 3. Job Detail
def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobportal/job_detail.html', {'job': job})

# 4. Apply Job
def apply_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        qualification = request.POST.get('qualification')
        resume = request.FILES.get('resume')

        Application.objects.create(
            job=job,
            full_name=full_name,
            email=email,
            phone=phone,
            qualification=qualification,
            resume=resume
        )
        return render(request, 'jobportal/success.html')
    return render(request, 'jobportal/apply.html', {'job': job})

# 5. Dashboard
def dashboard_view(request):
    if request.user.is_authenticated:
        user_applications = Application.objects.filter(email=request.user.email).order_by('-applied_at')
        return render(request, 'jobportal/dashboard.html', {'applications': user_applications})
    return redirect('login')

# 6. Authentication
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'jobportal/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'jobportal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# 7. Static Pages
def about_view(request):
    return render(request, 'jobportal/about.html')

def contact_view(request):
    return render(request, 'jobportal/contact.html')

def hire_talent(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        messages.success(request, f"Thank you {company_name}! We will contact you regarding the {role} role.")
        return redirect('home')
        
    return render(request, 'jobportal/hire_talent.html')
