
from django.shortcuts import render,get_object_or_404,redirect
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application



def signup(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return render(
                request,
                'accounts/signup_success.html'
            )

    else:
        form = SignUpForm()

    return render(
        request,
        'accounts/signup.html',
        {'form': form}
    )


@login_required
def dashboard(request):

    profile = request.user.profile

    if profile.role == 'employer':
        my_jobs=request.user.posted_jobs.all()
        total_jobs=my_jobs.count()
        total_applications = Application.objects.filter(
    job__employer=request.user
).count()
        return render(
            request,
            'dashboards/employer_dashboard.html',
            {
            'my_jobs':my_jobs,
            'total_jobs':total_jobs,
            'total_applications':total_jobs}
        )

    elif profile.role == 'job_seeker':

     total_jobs = Job.objects.filter(status='open').count()

     total_applications = Application.objects.filter(
        applicant=request.user
    ).count()
     my_applications = Application.objects.filter(
    applicant=request.user
).order_by('-applied_at')

     return render(
    request,
    'dashboards/seeker_dashboard.html',
    {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'my_applications': my_applications,
    }
     )
