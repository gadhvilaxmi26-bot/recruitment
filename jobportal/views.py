from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import ( authenticate, login, logout)

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Job, Application, HireTalent


def home_view(request):

    query = request.GET.get('search')

    if query:
        recent_jobs = Job.objects.filter(
            title__icontains=query
        ).order_by('-created_at')[:6]

    else:
        recent_jobs = Job.objects.all().order_by('-created_at')[:6]

    return render(
        request,
        'jobportal/index.html',
        {'recent_jobs': recent_jobs}
    )


def jobs_view(request):
    query = request.GET.get('search')

    if query:
        jobs = Job.objects.filter(
            title__icontains=query
        ).order_by('-created_at')
    else:
        jobs = Job.objects.all().order_by('-created_at')

    return render(
        request,
        'jobportal/jobs.html',
        {'jobs': jobs}
    )


def job_detail_view(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    return render(
        request,
        'jobportal/job_detail.html',
        {'job': job}
    )

@login_required
def apply_view(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':

        Application.objects.create(
            user=request.user,
            job=job,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            qualification=request.POST.get('qualification'),
            resume=request.FILES.get('resume')
        )

        messages.success(
            request,
            "Application submitted successfully."
        )

        return redirect('dashboard')

    return render(
        request,
        'jobportal/apply.html',
        {'job': job}
    )

    
@login_required
def dashboard_view(request):

    applications = Application.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_at')

    jobs_applied = applications.count()

    recent_applications = applications[:5]

    # Profile completion score (100 per field, max 1000)
    u = request.user
    score_fields = [
        u.username, u.email, u.first_name, u.last_name,
    ]
    filled = sum(1 for f in score_fields if f)
    profile_score = min(jobs_applied * 50 + filled * 100, 1000)

    context = {
        'applications': applications,
        'jobs_applied': jobs_applied,
        'recent_applications': recent_applications,
        'profile_score': profile_score,
    }

    return render(request, 'jobportal/dashboard.html', context)

    
# REGISTER
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully")

        return redirect('login')

    return render(request, 'jobportal/register.html')


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            messages.error(request, "Invalid username or password")

            return redirect('login')

    return render(request, 'jobportal/login.html')

# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('home')


# ABOUT
def about_view(request):

    return render(
        request,
        'jobportal/about.html'
    )


# CONTACT
def contact_view(request):

    return render(
        request,
        'jobportal/contact.html'
    )


# HIRE TALENT
def hire_talent(request):

    if request.method == 'POST':

        HireTalent.objects.create(
            company_name=request.POST.get('company_name'),
            industry=request.POST.get('industry'),
            email=request.POST.get('email'),
            role=request.POST.get('role'),
            requirements=request.POST.get('requirements')
        )

        messages.success(
            request,
            "Your hiring requirement has been submitted successfully."
        )

        return redirect('hire_talent')

    return render(
        request,
        'jobportal/hire_talent.html'
    )
