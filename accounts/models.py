from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    phone = models.CharField(
        max_length=20,
        blank=True
    )
    location = models.CharField(
        max_length=100,
        blank=True
    )
    company_name = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.user.username
