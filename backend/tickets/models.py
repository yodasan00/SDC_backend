# from django.db import models
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class Ticket(models.Model):

#     STATUS_CHOICES = (
#         ('PENDING', 'Pending Approval'),
#         ('APPROVED', 'Approved by DIT'),
#         ('REJECTED', 'Rejected by DIT'),
#         ('IN_PROGRESS', 'In Progress (SDC)'),
#         ('COMPLETED', 'Completed'),
#     )

#     DOMAIN_CHOICES = (
#     ('NONE', 'Unassigned'),
#     ('NETWORK', 'Network & Security'),
#     ('DB', 'Database Administration'),
#     ('SERVER', 'Server & Cloud'),
#     ('DEV', 'Software Development'),
#     )   

#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     created_by = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='tickets'
#     )
#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default='PENDING'
#     )
#     domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='NONE')
#     attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
#     pm_remarks = models.TextField(blank=True, null=True) 
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.status}"

# from django.conf import settings

# User = settings.AUTH_USER_MODEL


# class TicketComment(models.Model):
#     ticket = models.ForeignKey(
#         Ticket, on_delete=models.CASCADE, related_name="comments"
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Comment by {self.user} on Ticket {self.ticket.id}"


# class TicketAuditLog(models.Model):
#     ticket = models.ForeignKey(
#         Ticket, on_delete=models.CASCADE, related_name="audit_logs"
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     action = models.CharField(max_length=100)
#     remarks = models.TextField(blank=True, null=True)
#     old_status = models.CharField(max_length=20, blank=True)
#     new_status = models.CharField(max_length=20, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.action} - Ticket {self.ticket.id}"


from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Ticket(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved by DIT'),
        ('REJECTED', 'Rejected by DIT'),
        ('IN_PROGRESS', 'In Progress (SDC)'),
        ('COMPLETED', 'Completed'),
    )
    DOMAIN_CHOICES = (
    ('NONE', 'Unassigned'),
    ('NETWORK', 'Network & Security'),
    ('DB', 'Database Administration'),
    ('SERVER', 'Server & Cloud'),
    ('DEV', 'Software Development'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='NONE')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    pm_remarks = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

from django.conf import settings

User = settings.AUTH_USER_MODEL


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on Ticket {self.ticket.id}"


class TicketAuditLog(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="audit_logs"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - Ticket {self.ticket.id}"
