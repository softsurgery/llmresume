from .viewsets.resume_view import ResumeViewset
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = []

resume = csrf_exempt(ResumeViewset.as_view({'post': 'create'}))
resume_files = ResumeViewset.as_view({'get': 'files'})

urlpatterns += [
     path('resume/', resume, name='resume'),
     path('resume/<str:job_id>/files/', resume_files, name='resume_files'),
]