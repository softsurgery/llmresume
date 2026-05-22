from .viewsets.resume_view import ResumeViewset
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = []

resume = csrf_exempt(ResumeViewset.as_view({'post': 'create'}))


urlpatterns += [
     path('resume/', resume, name='resume'),
]