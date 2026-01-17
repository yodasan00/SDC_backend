from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ticket, TicketComment, TicketAuditLog
from .serializers import (
    TicketSerializer,
    TicketCommentSerializer,
    TicketAuditLogSerializer
)
from .permissions import (
    IsDepartmentUser,
    IsDITUser,
    IsSDCUser
)

# =====================================================
# PHASE 2 – DEPARTMENT APIs
# =====================================================

class CreateTicketAPIView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDepartmentUser]

    def perform_create(self, serializer):
        ticket = serializer.save(created_by=self.request.user)

        # Audit log
        TicketAuditLog.objects.create(
            ticket=ticket,
            user=self.request.user,
            action="Created ticket",
            old_status="",
            new_status=ticket.status
        )


class MyTicketsAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDepartmentUser]

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)


# =====================================================
# PHASE 3 – DIT APIs
# =====================================================

class PendingTicketsAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDITUser]

    def get_queryset(self):
        return Ticket.objects.filter(status='PENDING')


class ApproveTicketAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDITUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id, status='PENDING')
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found or already processed"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = ticket.status
        ticket.status = 'APPROVED'
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Approved ticket",
            old_status=old_status,
            new_status="APPROVED"
        )

        return Response(
            {"message": "Ticket approved successfully"},
            status=status.HTTP_200_OK
        )


class RejectTicketAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDITUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id, status='PENDING')
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found or already processed"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = ticket.status
        ticket.status = 'REJECTED'
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Rejected ticket",
            old_status=old_status,
            new_status="REJECTED"
        )

        return Response(
            {"message": "Ticket rejected successfully"},
            status=status.HTTP_200_OK
        )


# =====================================================
# PHASE 4 – SDC APIs
# =====================================================

class ApprovedTicketsAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsSDCUser]

    def get_queryset(self):
        return Ticket.objects.filter(status='APPROVED')


class StartWorkAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSDCUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id, status='APPROVED')
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found or not approved"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = ticket.status
        ticket.status = 'IN_PROGRESS'
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Started work",
            old_status=old_status,
            new_status="IN_PROGRESS"
        )

        return Response(
            {"message": "Work started on ticket"},
            status=status.HTTP_200_OK
        )


class CompleteTicketAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSDCUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id, status='IN_PROGRESS')
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found or not in progress"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = ticket.status
        ticket.status = 'COMPLETED'
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Completed ticket",
            old_status=old_status,
            new_status="COMPLETED"
        )

        return Response(
            {"message": "Ticket completed successfully"},
            status=status.HTTP_200_OK
        )


# =====================================================
# PHASE 6 – COMMENTS & AUDIT LOGS
# =====================================================

class AddCommentAPIView(generics.CreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketCommentsAPIView(generics.ListAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketComment.objects.filter(
            ticket_id=self.kwargs['ticket_id']
        )


class TicketAuditLogAPIView(generics.ListAPIView):
    serializer_class = TicketAuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketAuditLog.objects.filter(
            ticket_id=self.kwargs['ticket_id']
        )

from django.db.models import Count

class DepartmentDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentUser]

    def get(self, request):
        user = request.user

        data = {
            "total_tickets": Ticket.objects.filter(created_by=user).count(),
            "pending": Ticket.objects.filter(created_by=user, status="PENDING").count(),
            "approved": Ticket.objects.filter(created_by=user, status="APPROVED").count(),
            "rejected": Ticket.objects.filter(created_by=user, status="REJECTED").count(),
            "in_progress": Ticket.objects.filter(created_by=user, status="IN_PROGRESS").count(),
            "completed": Ticket.objects.filter(created_by=user, status="COMPLETED").count(),
        }

        return Response(data)

class DITDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDITUser]

    def get(self, request):
        data = {
            "pending": Ticket.objects.filter(status="PENDING").count(),
            "approved": Ticket.objects.filter(status="APPROVED").count(),
            "rejected": Ticket.objects.filter(status="REJECTED").count(),
            "total_tickets": Ticket.objects.count(),
        }

        return Response(data)

class SDCDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSDCUser]

    def get(self, request):
        data = {
            "approved": Ticket.objects.filter(status="APPROVED").count(),
            "in_progress": Ticket.objects.filter(status="IN_PROGRESS").count(),
            "completed": Ticket.objects.filter(status="COMPLETED").count(),
        }

        return Response(data)

class SystemReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDITUser]

    def get(self, request):
        data = {
            "total_tickets": Ticket.objects.count(),
            "by_status": Ticket.objects.values("status").annotate(count=Count("id")),
            "by_department": Ticket.objects.values(
                "created_by__username"
            ).annotate(count=Count("id")),
        }

        return Response(data)
