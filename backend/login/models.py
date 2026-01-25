from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    value = models.CharField(max_length=20, unique=True)
    display = models.CharField(max_length=100)

    def __str__(self):
        return self.display


class User(AbstractUser):

    ROLE_CHOICES = (
        ('DEPARTMENT', 'Department User'),
        ('DIT', 'Project Manager'),
        ('SDC', 'SDC Staff'),
        ('OFFICER', 'Officer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(unique= True, max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=False)
    department_name = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    domain = models.ForeignKey(
        Domain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
