from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser
    with additional fields for e-commerce
    """
    
    # Full Name - already inherited from AbstractUser (first_name, last_name)
    # but we can use full_name as a display field
    full_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Complete full name of the user"
    )
    
    # Email - already inherited from AbstractUser
    # Making it unique for authentication
    email = models.EmailField(
        unique=True,
        help_text="Email address for the user"
    )
    
    # Mobile Number
    mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Please enter a valid mobile number'
        )],
        unique=True,
        blank=True,
        null=True,
        help_text="Primary mobile number"
    )
    
    # Alternate Mobile Number
    alternate_mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Please enter a valid mobile number'
        )],
        blank=True,
        null=True,
        help_text="Alternate mobile number"
    )
    
    # Date of Birth
    dob = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth",
        help_text="Date of birth in YYYY-MM-DD format"
    )
    
    # Address
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Full residential address"
    )
    
    # Profile Image
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default='profile_images/default_profile.jpg',
        help_text="Profile picture of the user"
    )
    
    # Gender
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        help_text="Gender of the user"
    )
    
    # Additional Fields
    is_email_verified = models.BooleanField(
        default=False,
        help_text="Whether the email is verified"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Account creation timestamp"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last account update timestamp"
    )
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        db_table = 'custom_user'
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def get_full_name(self):
        """Return the full name of the user"""
        return self.full_name or f"{self.first_name} {self.last_name}".strip()
