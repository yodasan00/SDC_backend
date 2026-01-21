from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Ticket, TicketComment, TicketAuditLog
from .serializers import (
    TicketSerializer,
    TicketCommentSerializer,
    TicketAuditLogSerializer,
    TicketAssignSerializer
)
from .permissions import (
    IsDepartmentUser,
    IsDITUser,
    IsOfficer,
    IsSDCUser
)

# =====================================================
# PHASE 2 – DEPARTMENT APIs
# =====================================================

class CreateTicketAPIView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDepartmentUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        ticket = serializer.save(created_by=self.request.user)
        
        TicketAuditLog.objects.create(
            ticket=ticket, user=self.request.user, 
            action="Created ticket", new_status=ticket.status
        )


class MyTicketsAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsDepartmentUser]

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user).order_by('-created_at')


# =====================================================
# PHASE 3 – DIT APIs
# =====================================================

class DomainListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domains = [
            {"code": code, "label": label} 
            for code, label in Ticket.DOMAIN_CHOICES 
            if code != 'NONE' 
        ]
        return Response(domains)

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
        serializer = TicketAssignSerializer(data=request.data)
        
        if serializer.is_valid():
            selected_domain = serializer.validated_data['domain']
            remarks = request.data.get('remarks', '')
            
            old_status = ticket.status
            ticket.status = 'APPROVED'
            ticket.domain = selected_domain
            ticket.pm_remarks = remarks 
            ticket.save()

            TicketAuditLog.objects.create(
                ticket=ticket,
                user=request.user,
                action=f"Approved & Forwarded to {selected_domain}", 
                old_status=old_status,
                new_status=ticket.status,
                remarks=remarks 
            )

            return Response(
                {"message": f"Ticket approved and forwarded to {selected_domain} team successfully"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        remarks = request.data.get('remarks', '')
        old_status = ticket.status
        ticket.status = 'REJECTED'
        ticket.pm_remarks = remarks
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Rejected Ticket",
            old_status=old_status,
            new_status=ticket.status,
            remarks=remarks 
        )

        return Response(
            {"message": "Ticket rejected successfully"},
            status=status.HTTP_200_OK
        )

class DitHistoryAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(
            Q(status='APPROVED') | Q(status='REJECTED') | Q(status='COMPLETED') | Q(status='IN_PROGRESS')
        ).order_by('-created_at')


# =====================================================
# PHASE 4 – SDC APIs
# =====================================================

class ApprovedTicketsAPIView(generics.ListAPIView):
    """ The Inbox: Shows tickets assigned to SDC User's Domain """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsSDCUser]

    def get_queryset(self):
        user = self.request.user
        if user.domain == 'NONE':
            return Ticket.objects.none()

        return Ticket.objects.filter(
            status='APPROVED',
            domain=user.domain  
        )

# --- ADDED MISSING VIEW ---
class InProgressTicketsAPIView(generics.ListAPIView):
    """ Active Tasks: Tickets currently being worked on by SDC """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsSDCUser]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(
            status='IN_PROGRESS',
            domain=user.domain
        )

class StartWorkAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSDCUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(
                id=ticket_id, 
                status='APPROVED',
                domain=request.user.domain
            )
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found, not approved, or belongs to another domain"},
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
            ticket = Ticket.objects.get(
                id=ticket_id, 
                status='IN_PROGRESS',
                domain=request.user.domain 
            )
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found, not in progress, or belongs to another domain"},
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

class RevertTicketAPIView(APIView):

    permission_classes = [IsAuthenticated, IsSDCUser]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(
                id=ticket_id, 
                status='APPROVED', 
                domain=request.user.domain
            )
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Ticket not found or cannot be reverted."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        remarks = request.data.get('remarks', 'Reverted by SDC')

        ticket.status = 'PENDING'
        ticket.domain = 'NONE' 
        ticket.pm_remarks = f"{ticket.pm_remarks} \n[Revert Note]: {remarks}" 
        ticket.save()

        TicketAuditLog.objects.create(
            ticket=ticket,
            user=request.user,
            action="Reverted to PM",
            old_status='APPROVED',
            new_status=ticket.status,
            remarks=remarks 
        )

        return Response({"message": "Ticket reverted to Project Manager"}, status=status.HTTP_200_OK)
    

class SdcHistoryAPIView(generics.ListAPIView):
    """ History: Completed tickets for the SDC domain """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsSDCUser]

    def get_queryset(self):
        return Ticket.objects.filter(
            status='COMPLETED',
            domain=self.request.user.domain
        ).order_by('-created_at')


# =====================================================
# PHASE 5 – OFFICER APIs (Audit & Search)
# =====================================================

class OfficerStatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOfficer]

    def get(self, request):
        data = {
            "total_tickets": Ticket.objects.count(),
            "pending": Ticket.objects.filter(status="PENDING").count(),
            "approved": Ticket.objects.filter(status="APPROVED").count(),
            "rejected": Ticket.objects.filter(status="REJECTED").count(),
            "in_progress": Ticket.objects.filter(status="IN_PROGRESS").count(),
            "completed": Ticket.objects.filter(status="COMPLETED").count(),
        }
        return Response(data)


class OfficerTicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOfficer]
    
    # Using 'filters.SearchFilter' based on your import
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['title', 'description', 'status', 'domain', 'id']

    def get_queryset(self):
        # CORRECTED: Removed the duplicate method that filtered only 'COMPLETED'
        return Ticket.objects.all().order_by('-created_at')


# =====================================================
# PHASE 6 – COMMENTS & AUDIT LOGS
# =====================================================

class TicketDetailAPIView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    # CORRECTED: Your URL sends 'ticket_id', so we must tell Django to look for that
    lookup_url_kwarg = 'ticket_id' 

class AddCommentAPIView(generics.CreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket_instance = get_object_or_404(Ticket, id=ticket_id)
        serializer.save(user=self.request.user, ticket=ticket_instance)

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

# =====================================================
# PHASE 7 – DASHBOARD STATS
# =====================================================

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
        user_domain = request.user.domain
        data = {
            "approved": Ticket.objects.filter(status="APPROVED", domain=user_domain).count(),
            "in_progress": Ticket.objects.filter(status="IN_PROGRESS", domain=user_domain).count(),
            "completed": Ticket.objects.filter(status="COMPLETED", domain=user_domain).count(),
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