from django.shortcuts import render
from .models import Job


# Create your views here.

def home(request):

    latest_jobs = Job.objects.filter(
        status='open'
    ).order_by('-created_at')[:5]

    return render(
        request,
        'home.html',
        {'latest_jobs': latest_jobs}
    )



def job_list(request):

    jobs = Job.objects.filter(status='open')

    # Get search values from URL
    title = request.GET.get('title', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    job_type = request.GET.get('job_type', '')

    # Apply search and filters
    if title:
        jobs = jobs.filter(title__icontains=title)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if category:
        jobs = jobs.filter(category__icontains=category)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    jobs = jobs.order_by('-created_at')

    context = {
        'jobs': jobs,
        'title': title,
        'location': location,
        'category': category,
        'job_type': job_type,
        'job_types': Job.JOB_TYPE_CHOICES,
    }

    return render(request, 'jobs/job_list.html', context)

