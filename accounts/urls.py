from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
     path(
        'login/',auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    path(
        'logout/',auth_views.LogoutView.as_view(),name='logout'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('profile/', views.seeker_profile, name='profile'),
        path('profile/', views.employer_profile, name='profile'),
        path('edit-profile/', views.edit_profile, name='edit_profile'),
        path('edit-profile/', views.edit_profile, name='edit_profile'),
]