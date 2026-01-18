from rest_framework import serializers
from .models import Ticket, TicketComment, TicketAuditLog




class TicketSerializer(serializers.ModelSerializer):

    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'created_at',
            'created_by',
            'created_by_name',
        ]

        # 🔥 THIS IS THE FIX
        read_only_fields = [
            'created_by',
            'status',
            'created_at',
        ]

    def get_created_by_name(self, obj):
        user = obj.created_by
        if user.get_full_name():
            return user.get_full_name()
        return user.username







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
