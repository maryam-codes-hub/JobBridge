from django.shortcuts import render,redirect
from jobs.models import Job
from django.shortcuts import  get_object_or_404
from django.contrib.auth.decorators import login_required
from applications.forms import ApplicationForm,Application
from django.contrib import messages

# Create your views here.


def home(request):

    # latest_jobs = Job.objects.filter(
    #     status='open'
    # ).order_by('-created_at')[:5]


    # context = {
    #     'latest_jobs': latest_jobs,
        
    # }

    return render(request, 'home.html')




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

def job_detail(request, id):

    job = get_object_or_404(Job, id=id)

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job}
    )
@login_required
def apply_job(request, id):

    # Step 1: Database se correct job retrieve karo
    job = get_object_or_404(Job, id=id)

    # Step 2: Check karo user ne pehle apply to nahi kiya
    already_applied = Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if already_applied:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', id=job.id)

    # Step 3: GET request par empty form
    if request.method == 'GET':
        form = ApplicationForm()

    # Step 4: POST request par submitted data
    elif request.method == 'POST':
        form = ApplicationForm(request.POST)

        # Step 5: Form validation
        if form.is_valid():

            # Step 6: Database mein abhi save nahi karna
            application = form.save(commit=False)

            # Step 7: Job attach karo
            application.job = job

            # Step 8: Logged-in user attach karo
            application.applicant = request.user

            # Step 9: Database mein save karo
            application.save()

            # Step 10: Success notification
            messages.success(
                request,
                'Your application has been submitted successfully!'
            )

            return redirect('job_detail', id=job.id)

    # Step 11: Form page display karo
    return render(request, 'applications/apply.html', {
        'form': form,
        'job': job
    })

@login_required
def job_applications(request, id):

    job = get_object_or_404(Job, id=id)
    if job.employer != request.user:
     return redirect('dashboard')
    applications = job.applications.all().order_by('-applied_at')
    return render(
    request,
    'applications/job_applications.html',
    {
        'job': job,
        'applications': applications
    }
)