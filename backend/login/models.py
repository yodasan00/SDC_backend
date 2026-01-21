from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('DEPARTMENT', 'Department User'),
        ('DIT', 'Project Manager'),
        ('SDC', 'SDC Staff'),
        ('OFFICER', 'Officer'), #view only access
    )
    DOMAIN_CHOICES = (
    ('NONE', 'Unassigned'),
    ('NETWORK', 'Network & Security'),
    ('DB', 'Database Administration'),
    ('SERVER', 'Server & Cloud'),
    ('DEV', 'Software Development'),
    )   

    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='NONE')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
