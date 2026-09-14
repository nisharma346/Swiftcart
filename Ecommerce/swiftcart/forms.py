from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Contact
import re

class ContactForm(forms.ModelForm):

    class Meta:

        model = Contact

        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Your Name"
            }),

            "email": forms.EmailInput(attrs={
                "class":"form-control",
                "placeholder":"Email Address"
            }),

            "subject": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Subject"
            }),

            "message": forms.Textarea(attrs={
                "class":"form-control",
                "rows":6,
                "placeholder":"Write your message..."
            }),

        }


class CustomUserRegistrationForm(UserCreationForm):
    """
    Registration form for CustomUser model
    """
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name'
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        }),
        label='Email Address'
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        }),
        help_text='Password must be at least 8 characters long and contain numbers and special characters.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the help text from password1
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def clean_full_name(self):
        """Validate full name"""
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip()) == 0:
            raise forms.ValidationError('Full name cannot be empty.')
        if not re.match(r'^[a-zA-Z\s]+$', full_name):
            raise forms.ValidationError('Full name can only contain letters and spaces.')
        return full_name
    
    def clean_password1(self):
        """Validate password strength"""
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[0-9]', password1):
            raise forms.ValidationError('Password must contain at least one number.')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password1):
            raise forms.ValidationError('Password must contain at least one special character.')
        return password1
    
    def save(self, commit=True):
        """Save the user with the full_name field"""
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('email')  # Use email as username
        
        if commit:
            user.save()
        return user


class UserProfileEditForm(forms.ModelForm):
    """
    Form for updating CustomUser profile data safely.
    Handles optional mobile_no and unique constraint validation.
    """
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'mobile_no',
            'alternate_mobile_no',
            'dob',
            'gender',
            'address',
            'profile_image',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'alternate_mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = False
        self.fields['mobile_no'].required = False
        self.fields['alternate_mobile_no'].required = False
        self.fields['dob'].required = False
        self.fields['gender'].required = False
        self.fields['address'].required = False
        self.fields['profile_image'].required = False

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get('mobile_no')
        if not mobile_no or not str(mobile_no).strip():
            return None
        mobile_no = str(mobile_no).strip()
        if CustomUser.objects.filter(mobile_no=mobile_no).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This mobile number is already registered with another account.')
        return mobile_no

    def clean_alternate_mobile_no(self):
        alt_mobile = self.cleaned_data.get('alternate_mobile_no')
        if not alt_mobile or not str(alt_mobile).strip():
            return None
        return str(alt_mobile).strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError('Email address cannot be empty.')
        email = email.strip().lower()
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already registered with another account.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.email:
            user.username = user.email  # Keep username in sync with email
        if commit:
            user.save()
        return user

