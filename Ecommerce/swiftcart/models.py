from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.text import slugify

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


class Category(models.Model):
    """Product category model for organizing products."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from decimal import Decimal
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    category = models.ForeignKey(
    "Category",
    on_delete=models.CASCADE,
    related_name="products",
    null=True,
    blank=True
)

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="products/"
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount = models.PositiveIntegerField(
        default=0,
        help_text="Enter discount in percentage"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    stock = models.PositiveIntegerField(default=0)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.5
    )

    review_count = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    is_best_seller = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        if self.original_price:
            discount_amount = (
                self.original_price * Decimal(self.discount)
            ) / Decimal("100")

            self.price = self.original_price - discount_amount

        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        return self.discount

    def __str__(self):
        return self.name
class GalleryImage(models.Model):
    """Gallery image model for showcasing images on the site."""

    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title or self.image.name
class TeamMember(models.Model):
    employee_image = models.ImageField(upload_to="team/")
    employee_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.employee_name
class Order(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    mobile = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    message = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message

