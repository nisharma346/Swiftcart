from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Contact

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


class ContactForm(forms.Form):
    """Simple contact form for customer inquiries."""
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name',
        }),
        label='Name'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email',
        }),
        label='Email'
    )
    subject = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
        }),
        label='Subject'
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message',
            'rows': 5,
        }),
        label='Message'
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) == 0:
            raise forms.ValidationError('Please enter your name.')
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Message should be at least 10 characters long.')
        return message
