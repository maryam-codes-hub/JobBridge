
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

@login_required
def seeker_profile(request):
    user_profile = request.user.profile

    return render(request, 'accounts/seeker_profile.html', {
        'user_profile': user_profile
    })

@login_required
def employer_profile(request):
    user_profile = request.user.profile

    return render(request, 'accounts/employer_profile.html', {
        'user_profile': user_profile
    })

@login_required
def edit_profile(request):

    user = request.user
    user_profile = request.user.profile

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user_profile.phone = request.POST.get('phone')
        user_profile.location = request.POST.get('location')

        # Employer specific field
        if user_profile.role == 'employer':
            user_profile.company_name = request.POST.get('company_name')

        user.save()
        user_profile.save()

        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {
        'user': user,
        'user_profile': user_profile
    })