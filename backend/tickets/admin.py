from django.contrib import admin
from .models import Ticket, TicketComment, TicketAuditLog

admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(TicketAuditLog)

# Register your models here.
