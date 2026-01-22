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

<<<<<<< Updated upstream
=======
    DEPARTMENT_CHOICES = (
        ('', 'None'),
        ('IT Dept', 'IT Dept'),
        ('Cisco Dept', 'Cisco Dept'),
    )

    DOMAIN_CHOICES = (
    ('NONE', 'Unassigned'),
    ('NETWORK', 'Network & Security'),
    ('DB', 'Database Administration'),
    ('SERVER', 'Server & Cloud'),
    ('DEV', 'Software Development'),
    ) 

>>>>>>> Stashed changes
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='NONE')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department_name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='NONE', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


