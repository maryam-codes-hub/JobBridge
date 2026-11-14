
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES
    )

    phone = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=100, required=False)
    company_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
        )
    
    def clean(self):

        cleaned_data = super().clean()

        role = cleaned_data.get('role')
        company_name = cleaned_data.get('company_name')

        if role == 'employer' and not company_name:
            self.add_error(
                'company_name',
                'Company name is required for employers.'
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone'],
                location=self.cleaned_data['location'],
                company_name=self.cleaned_data['company_name']
            )

        return user
