from django.db import models
from django.conf import settings
from datetime import timedelta
from login.models import Domain

User = settings.AUTH_USER_MODEL


# =========================
# MASTER TABLES
# =========================

class TicketType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RequestType(models.Model):
    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE,
        related_name='request_types'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('ticket_type', 'name')

    def __str__(self):
        return f"{self.ticket_type.name} - {self.name}"


# =========================
# MAIN TICKET MODEL
# =========================

class Ticket(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved by DIT'),
        ('REJECTED', 'Rejected by DIT'),
        ('IN_PROGRESS', 'In Progress (SDC)'),
        ('COMPLETED', 'Completed'),
        ('CLOSED', 'Closed')
    )

    PRIORITY_CHOICES = (
        ('P1', 'P1 - 30 Minutes'),
        ('P2', 'P2 - 2 Hours'),
        ('P3', 'P3 - 1 Day'),
        ('P4', 'P4 - 2 Days'),
    )

    PRIORITY_SLA_MAP = {
        'P1': timedelta(minutes=30),
        'P2': timedelta(hours=2),
        'P3': timedelta(days=1),
        'P4': timedelta(days=2),
    }

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets'
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )

    domain = models.ForeignKey(
        Domain, on_delete=models.SET_NULL, null=True, blank=True
    )

    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default='P3'
    )

    sla_time = models.DurationField(
        null=True,
        blank=True,
        help_text="SLA duration based on priority"
    )

    # ✅ NEW REQUIRED FIELDS
    affected_end_user = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    request_type = models.ForeignKey(
        RequestType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    pm_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sla_time:
            self.sla_time = self.PRIORITY_SLA_MAP.get(self.priority)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} [{self.priority}] - {self.status}"


# =========================
# COMMENTS
# =========================

class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on Ticket {self.ticket.id}"


# =========================
# AUDIT LOG
# =========================

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
