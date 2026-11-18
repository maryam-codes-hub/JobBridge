
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:id>/', views.job_detail, name='job_detail'),
    path('<int:id>/apply/', views.apply_job, name='apply_job'),
    path(
    'employer/jobs/<int:id>/applications/',
    views.job_applications,
    name='job_applications'
),
path('employer/post-job/', views.post_job, name='post_job'),
path(
    'employer/applications/<int:id>/update-status/',
    views.update_application_status,
    name='update_application_status'
),
]
