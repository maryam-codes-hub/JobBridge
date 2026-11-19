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

@login_required
def post_job(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        category = request.POST.get('category')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        deadline = request.POST.get('deadline')

        Job.objects.create(
            employer=request.user,
            title=title,
            category=category,
            location=location,
            job_type=job_type,
            salary=salary,
            description=description,
            requirements=requirements,
            deadline=deadline if deadline else None
        )

        return redirect('dashboard')

    return render(request, 'jobs/post_job.html')
@login_required
def update_application_status(request, id):
    application = get_object_or_404(Application, id=id)
    if application.job.employer != request.user:
     return redirect('dashboard')
    if request.method == 'POST':

     new_status = request.POST.get('status')
    if new_status in dict(Application.STATUS_CHOICES):

     application.status = new_status

     application.save()
     return redirect('job_applications', id=application.job.id)
    return redirect('job_applications', id=application.job.id)



@login_required
def edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if job.employer != request.user:
        return redirect('dashboard')

    if request.method == 'POST':

        job.title = request.POST.get('title')
        job.category = request.POST.get('category')
        job.location = request.POST.get('location')
        job.job_type = request.POST.get('job_type')
        job.salary = request.POST.get('salary')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')

        deadline = request.POST.get('deadline')
        job.deadline = deadline if deadline else None

        job.save()

        return redirect('dashboard')

    return render(request, 'jobs/edit_job.html', {
        'job': job
    })

@login_required
def edit_application(request, id):

    application = get_object_or_404(Application,id=id)
    if application.applicant != request.user:
        return redirect('dashboard')
    if request.method=='POST':
        application.cover_letter=request.POST.get('cover_letter')
        application.save()
        
        return redirect('dashboard')

    return render(request, 'applications/edit_application.html', {
        'application': application
    })
@login_required
def delete_application(request, id):

    application = get_object_or_404(Application, id=id)

    if application.applicant != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        application.delete()
        return redirect('dashboard')

    return redirect('dashboard')

login_required
def delete_job(request,id):

    job= get_object_or_404(Job, id=id)

    if job.employer != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        job.delete()
        return redirect('dashboard')

    return redirect('dashboard')