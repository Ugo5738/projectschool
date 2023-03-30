from accounts.models import LEVEL, Student, User
from course.models import Course, Program
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserChangeForm, UserCreationForm)
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Email"), widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter your Email"}))
    first_name = forms.CharField(required=True, label=_("First Name"), widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter your First Name"}))
    last_name = forms.CharField(required=True, label=_("Last Name"), widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter your Last Name"}))
    newsletter = forms.BooleanField(required=False, label=_("Subscribe to newsletter"))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email.')
        return email
        
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", "first_name", "last_name", "phone", "address", "picture", "newsletter")


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, label=_("Email"))
    
    class Meta:
        model = User
        fields = ("username", "password")


class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="Username")

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="First Name")

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="Last Name")

    address = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="Address")

    phone = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="Mobile Number")

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3', }),
        label="Email")

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control mb-3', }),
        label="Password")

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control mb-3', }),
        label="Password Confirmation")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control mb-3',
                'id': 'username_id'
            }
        ),
        label="Username",
    )

    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control mb-3',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control mb-3',
            }
        ),
        label="Mobile Number",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control mb-3',
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control mb-3',
            }
        ),
        label="Last name",
    )

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                'class': 'browser-default custom-select form-control mb-3',
            }
        ),
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control mb-3'}),
        label="Course",
    )

    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control mb-3'}),
        label="Program",  # Department",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control mb-3',
            }
        ),
        label="Email Address",
    )

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control mb-3', }),
        label="Password", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control mb-3', }),
        label="Password Confirmation", )


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email.')
        return email
        

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(
            student=user,
            level=self.cleaned_data.get('level'),
            course=self.cleaned_data.get('course'),
            program=self.cleaned_data.get('program')
        )
        student.save()
        return user


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control mb-3'}),
        label="Email Address")

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3'}),
        label="First Name")

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3'}),
        label="Last Name")

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3'}),
        label="Phone Number")

    address = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-3'}),
        label="Address / city")

    class Meta:
        model = User
        fields = ['email', 'phone', 'address', 'picture', 'first_name', 'last_name']


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address. "
            self.add_error('email', msg)
            return email
