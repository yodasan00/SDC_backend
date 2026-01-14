from rest_framework import serializers
from .models import Ticket, TicketComment, TicketAuditLog

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['created_by', 'status', 'created_at']




class TicketCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketComment
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class TicketAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketAuditLog
        fields = "__all__"
