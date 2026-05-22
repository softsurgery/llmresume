"""
URL configuration for api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from resumes.views import download_file

applications = ['resumes']
urlpatterns = [path("api/", include(f"{app}.urls")) for app in applications]

urlpatterns += [
    path('download/<str:job_id>/<str:filename>', download_file, name='download_file'),
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
