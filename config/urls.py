from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Naya add karein
from django.conf.urls.static import static # Naya add karein

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobportal.urls')),
]

# Yeh line add karni hai taaki media files (resumes) access ho sakein
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)