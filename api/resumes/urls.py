from .viewsets.resume_view import ResumeViewset
from django.urls import path

urlpatterns = []

resume = ResumeViewset.as_view({'post': 'create'})


urlpatterns += [
     path('resume/', resume, name='resume'),
]