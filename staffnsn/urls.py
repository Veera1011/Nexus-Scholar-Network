from django.urls import path
from .views import Staffdashboard

urlpatterns = [
    
    path('staff/dash/', Staffdashboard.as_view(), name='staffdashboard'),
]
