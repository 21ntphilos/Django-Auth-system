from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin

# Create your models here.
class UserModel(AbstractUser, BaseUserManager):
    def create_user(self, email,full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, full_name, **extra_fields)
