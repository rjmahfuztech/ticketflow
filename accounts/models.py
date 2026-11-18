from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"

    ROLE_CHOICES = [(CUSTOMER, "Customer"), (AGENT, "Agent"), (ADMIN, "Admin")]

    username = None
    first_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = CloudinaryField(
        "profile_image", asset_folder="profile_image", blank=True, null=True
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=CUSTOMER, db_index=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
