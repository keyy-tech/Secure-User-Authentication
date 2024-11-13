import random
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def validate_eight_digits(value):
    if not (10000000 <= value <= 99999999):
        raise ValidationError("ID must be an 8-digit number.")

def generate_unique_id():
    while True:
        new_id = random.randint(10000000, 99999999)
        if not ProfileUser.objects.filter(profile_id=new_id).exists():
            return new_id

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"  # Use email to log in
    REQUIRED_FIELDS = []  # Required fields when creating a user

    def __str__(self):
        return self.username

class ProfileUser(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    ADMIN = 'Admin'
    USER = 'User'
    GUEST = 'Guest'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (GUEST, 'Guest')
    ]

    profile_id = models.PositiveIntegerField(
        primary_key=True,
        validators=[validate_eight_digits],
        default=generate_unique_id,
        editable=False,
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=None)
    date_of_birth = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)