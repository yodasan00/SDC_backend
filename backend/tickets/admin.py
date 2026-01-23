# from django.contrib import admin
# from .models import Ticket, TicketComment, TicketAuditLog

# admin.site.register(Ticket)
# admin.site.register(TicketComment)
# admin.site.register(TicketAuditLog)

# # Register your models here.


# from django.contrib import admin
# from .models import Ticket, TicketComment, TicketAuditLog


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'title', 'priority', 'sla_time',
#         'status', 'domain', 'created_by', 'created_at'
#     )

#     list_filter = ('priority', 'status', 'domain')
#     search_fields = ('title', 'description')
#     ordering = ('-created_at',)

#     fields = (
#         'title',
#         'description',
#         'priority',
#         'sla_time',
#         'status',
#         'domain',
#         'attachment',
#         'pm_remarks',
#         'created_by'
#     )

#     readonly_fields = ('created_at',)


# admin.site.register(TicketComment)
# admin.site.register(TicketAuditLog)


from django.contrib import admin
from .models import (
    Ticket,
    TicketComment,
    TicketAuditLog,
    TicketType,
    RequestType
)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'priority',
        'ticket_type',
        'request_type',
        'affected_end_user',
        'status',
        'domain',
        'created_at',
    )

    list_filter = ('priority', 'ticket_type', 'status', 'domain')
    search_fields = ('title', 'affected_end_user')
    ordering = ('-created_at',)


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ticket_type')
    list_filter = ('ticket_type',)
    search_fields = ('name',)


admin.site.register(TicketComment)
admin.site.register(TicketAuditLog)
