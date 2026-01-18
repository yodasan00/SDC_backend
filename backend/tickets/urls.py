from django.urls import path
from .views import (
    CreateTicketAPIView, DitHistoryAPIView, MyTicketsAPIView, 
    PendingTicketsAPIView, ApproveTicketAPIView, RejectTicketAPIView,
    ApprovedTicketsAPIView, SdcHistoryAPIView, StartWorkAPIView, CompleteTicketAPIView,
    AddCommentAPIView, TicketCommentsAPIView, TicketAuditLogAPIView,
    DepartmentDashboardStatsAPIView, DITDashboardStatsAPIView, SDCDashboardStatsAPIView,
    SystemReportAPIView, InProgressTicketsAPIView, TicketDetailAPIView,
)

urlpatterns = [
    # --- Department --
    path('create/', CreateTicketAPIView.as_view(), name='create-ticket'),
    path('my-tickets/', MyTicketsAPIView.as_view(), name='my-tickets'),
    path('dashboard/department/', DepartmentDashboardStatsAPIView.as_view(), name='dept-stats'),

    # --- DIT ---
    path('pending/', PendingTicketsAPIView.as_view(), name='pending-tickets'),
    path('<int:ticket_id>/approve/', ApproveTicketAPIView.as_view(), name='approve-ticket'),
    path('<int:ticket_id>/reject/', RejectTicketAPIView.as_view(), name='reject-ticket'),
    path('dashboard/dit/', DITDashboardStatsAPIView.as_view(), name='dit-stats'),
    path('dit/history/', DitHistoryAPIView.as_view(), name='dit-history'),
    # --- SDC ---
    path('approved/', ApprovedTicketsAPIView.as_view(), name='approved-tickets'),
    path('in-progress/', InProgressTicketsAPIView.as_view(), name='in-progress-tickets'),
    path('<int:ticket_id>/start/', StartWorkAPIView.as_view(), name='start-ticket'),
    path('<int:ticket_id>/complete/', CompleteTicketAPIView.as_view(), name='complete-ticket'),
    path('dashboard/sdc/', SDCDashboardStatsAPIView.as_view(), name='sdc-stats'),
    path('sdc/history/', SdcHistoryAPIView.as_view(), name='sdc-history'),

    # --- Comments/Logs ---
    # Removed 'tickets/' here too
    path('<int:ticket_id>/comments/add/', AddCommentAPIView.as_view(), name='add-comment'),
    path('<int:ticket_id>/comments/', TicketCommentsAPIView.as_view(), name='view-comments'),
    path('<int:ticket_id>/audit-log/', TicketAuditLogAPIView.as_view(), name='audit-log'),
    path('<int:id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    
    # --- Reports ---
    path('reports/system/', SystemReportAPIView.as_view(), name='system-report'),
]