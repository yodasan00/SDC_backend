# from django.urls import path
# from .views import (
#     CreateTicketAPIView, DomainListAPIView, MyTicketsAPIView, OfficerTicketListAPIView, 
#     PendingTicketsAPIView, ApproveTicketAPIView, RejectTicketAPIView,
#     ApprovedTicketsAPIView, RevertTicketAPIView,SdcHistoryAPIView, StartWorkAPIView, CompleteTicketAPIView,
#     AddCommentAPIView, TicketCommentsAPIView, TicketAuditLogAPIView,
#     DepartmentDashboardStatsAPIView, DITDashboardStatsAPIView, SDCDashboardStatsAPIView,
#     SystemReportAPIView,OfficerStatsAPIView, TicketDetailAPIView,DitHistoryAPIView, InProgressTicketsAPIView
# )

# urlpatterns = [
#     # --- Department --
#     path('create/', CreateTicketAPIView.as_view(), name='create-ticket'),
#     path('my-tickets/', MyTicketsAPIView.as_view(), name='my-tickets'),
#     path('dashboard/department/', DepartmentDashboardStatsAPIView.as_view(), name='dept-stats'),

#  # --- Project Manager ---
#     path('domains/', DomainListAPIView.as_view(), name='domain-list'),
#     path('pending/', PendingTicketsAPIView.as_view(), name='pending-tickets'),
#     path('<int:ticket_id>/approve/', ApproveTicketAPIView.as_view(), name='approve-ticket'),
#     path('<int:ticket_id>/reject/', RejectTicketAPIView.as_view(), name='reject-ticket'),
#     path('dashboard/dit/', DITDashboardStatsAPIView.as_view(), name='dit-stats'),
#     path('dit/history/', DitHistoryAPIView.as_view(), name='dit-history'),

#     # --- DIT ---
#     path('pending/', PendingTicketsAPIView.as_view(), name='pending-tickets'),
#     path('<int:ticket_id>/approve/', ApproveTicketAPIView.as_view(), name='approve-ticket'),
#     path('<int:ticket_id>/reject/', RejectTicketAPIView.as_view(), name='reject-ticket'),
#     path('dashboard/dit/', DITDashboardStatsAPIView.as_view(), name='dit-stats'),
#     path('dit/history/', DitHistoryAPIView.as_view(), name='dit-history'),
#     # --- SDC ---
#     path('approved/', ApprovedTicketsAPIView.as_view(), name='approved-tickets'),
#     path('in-progress/', InProgressTicketsAPIView.as_view(), name='in-progress-tickets'),
#     path('<int:ticket_id>/start/', StartWorkAPIView.as_view(), name='start-ticket'),
#     path('<int:ticket_id>/complete/', CompleteTicketAPIView.as_view(), name='complete-ticket'),
#     path('dashboard/sdc/', SDCDashboardStatsAPIView.as_view(), name='sdc-stats'),
#     path('sdc/history/', SdcHistoryAPIView.as_view(), name='sdc-history'),


#       # OFFICER (AUDIT) URLS
#     path('officer/stats/', OfficerStatsAPIView.as_view(), name='officer-stats'),
#     path('officer/all/', OfficerTicketListAPIView.as_view(), name='officer-all-tickets'),

#     # --- Comments/Logs ---
#     # Removed 'tickets/' here too
#     path('<int:ticket_id>/comments/add/', AddCommentAPIView.as_view(), name='add-comment'),
#     path('<int:ticket_id>/comments/', TicketCommentsAPIView.as_view(), name='view-comments'),
#     path('<int:ticket_id>/audit-log/', TicketAuditLogAPIView.as_view(), name='audit-log'),
#     path('<int:id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    
#     # --- Reports ---
#     path('reports/system/', SystemReportAPIView.as_view(), name='system-report'),
# ]


from django.urls import path
from .views import (

    CreateTicketAPIView, DomainListAPIView, MyTicketsAPIView, OfficerTicketListAPIView, 
    PendingTicketsAPIView, ApproveTicketAPIView, RejectTicketAPIView,
    ApprovedTicketsAPIView, RevertTicketAPIView,SdcHistoryAPIView, StartWorkAPIView, CompleteTicketAPIView,
    AddCommentAPIView, TicketCommentsAPIView, TicketAuditLogAPIView,
    DepartmentDashboardStatsAPIView, DITDashboardStatsAPIView, SDCDashboardStatsAPIView,
    SystemReportAPIView,OfficerStatsAPIView, TicketDetailAPIView,DitHistoryAPIView, InProgressTicketsAPIView,
    TicketTypeListAPIView, RequestTypeListAPIView, TicketPriorityListAPIView
)

urlpatterns = [
    # --- Department --
    path('create/', CreateTicketAPIView.as_view(), name='create-ticket'),
    path('my-tickets/', MyTicketsAPIView.as_view(), name='my-tickets'),
    path('dashboard/department/', DepartmentDashboardStatsAPIView.as_view(), name='dept-stats'),

    # --- Project Manager ---
    path('domains/', DomainListAPIView.as_view(), name='domain-list'),
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
    path('<int:ticket_id>/revert/', RevertTicketAPIView.as_view(), name='revert-ticket'),
    path('sdc/history/', SdcHistoryAPIView.as_view(), name='sdc-history'),

    # OFFICER (AUDIT) URLS
    path('officer/stats/', OfficerStatsAPIView.as_view(), name='officer-stats'),
    path('officer/all/', OfficerTicketListAPIView.as_view(), name='officer-all-tickets'),

    # --- Comments/Logs ---
    # Removed 'tickets/' here too
    path('<int:ticket_id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    path('<int:ticket_id>/comments/add/', AddCommentAPIView.as_view(), name='add-comment'),
    path('<int:ticket_id>/comments/', TicketCommentsAPIView.as_view(), name='view-comments'),
    path('<int:ticket_id>/audit-log/', TicketAuditLogAPIView.as_view(), name='audit-log'),
    path('<int:id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    
    # --- Reports ---
    path('reports/system/', SystemReportAPIView.as_view(), name='system-report'),

    
    # --- Fetch Tickets ---
    path('ticket-types/', TicketTypeListAPIView.as_view(), name='ticket-types'),
    path('request-types/', RequestTypeListAPIView.as_view(), name='request-types'),

    # Get Prorities
    path('ticket-priorities/', TicketPriorityListAPIView.as_view(), name='ticket-priorities'),
]