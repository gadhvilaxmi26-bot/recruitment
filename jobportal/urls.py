from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.jobs_view, name='jobs'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('hire_talent/', views.hire_talent, name='hire_talent'),
    path('apply/<int:job_id>/', views.apply_view, name='apply'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
]
