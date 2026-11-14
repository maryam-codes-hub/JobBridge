
from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'employer',
       
        'job_type',
        'status',
        
    )

    search_fields = (
        'title',
        'category',
        'location',
    )

    list_filter = (
        'status',
        'job_type',
        'location',
    )

    ordering = ('-created_at',)


