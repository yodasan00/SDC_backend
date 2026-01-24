# from rest_framework import serializers
# from .models import Ticket, TicketComment, TicketAuditLog




# class TicketSerializer(serializers.ModelSerializer):

#     created_by_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Ticket
#         fields = [
#             'id',
#             'title',
#             'description',
#             'status',
#             'created_at',
#             'created_by',
#             'created_by_name',
#             'domain',
#             'attachment',
#         ]

#         read_only_fields = [
#             'created_by',
#             'status',
#             'created_at',
#             'pm_remarks'
#         ]

#     def get_created_by_name(self, obj):
#         user = obj.created_by
#         if user.get_full_name():
#             return user.get_full_name()
#         return user.username




# class TicketCommentSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True) 
#     ticket = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = TicketComment
#         fields = ['id', 'ticket', 'user', 'comment', 'created_at']


# class TicketAuditLogSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = TicketAuditLog
#         fields = "__all__"

# class TicketAssignSerializer(serializers.ModelSerializer):

#     domain = serializers.ChoiceField(choices=Ticket.DOMAIN_CHOICES)

#     class Meta:
#         model = Ticket
#         fields = ['domain']


# from rest_framework import serializers
# from .models import Ticket, TicketComment, TicketAuditLog


# class TicketSerializer(serializers.ModelSerializer):

#     created_by_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Ticket
#         fields = [
#             'id',
#             'title',
#             'description',
#             'status',
#             'priority',       # ✅ NEW
#             'sla_time',       # ✅ NEW
#             'created_at',
#             'created_by',
#             'created_by_name',
#             'domain',
#             'attachment',
#         ]

#         read_only_fields = [
#             'created_by',
#             'status',
#             'created_at',
#             'pm_remarks',
#             'sla_time',  # SLA controlled internally/admin
#         ]

#     def get_created_by_name(self, obj):
#         user = obj.created_by
#         return user.get_full_name() or user.username


# class TicketCommentSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     ticket = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = TicketComment
#         fields = ['id', 'ticket', 'user', 'comment', 'created_at']


# class TicketAuditLogSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = TicketAuditLog
#         fields = "__all__"


# class TicketAssignSerializer(serializers.ModelSerializer):
#     domain = serializers.ChoiceField(choices=Ticket.DOMAIN_CHOICES)

#     class Meta:
#         model = Ticket
#         fields = ['domain']


from rest_framework import serializers

from login.models import Domain
from .models import (
    Ticket,
    TicketComment,
    TicketAuditLog,
    TicketType,
    RequestType
)


class TicketSerializer(serializers.ModelSerializer):

    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'sla_time',
            'affected_end_user',
            'ticket_type',
            'request_type',
            'created_at',
            'created_by',
            'created_by_name',
            'domain',
            'attachment',
        ]

        read_only_fields = [
            'created_by',
            'status',
            'created_at',
            'pm_remarks',
            'sla_time',
        ]

    def get_created_by_name(self, obj):
        user = obj.created_by
        return user.get_full_name() or user.username


class TicketCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'user', 'comment', 'created_at']


class TicketAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketAuditLog
        fields = "__all__"


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'name']


class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestType
        fields = ['id', 'name', 'ticket_type']


class TicketAssignSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(
        slug_field='value', 
        queryset=Domain.objects.all()
    )

    class Meta:
        model = Ticket  # Point this to Ticket, not Domain
        fields = ['domain']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'value', 'display']
