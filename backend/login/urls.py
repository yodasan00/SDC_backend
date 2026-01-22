from django.urls import path
from .views import  LoginAPIView, RegistrationView, ListUsersAPIView, UpdateUserAPIView
from .views import LoginAPIView, RegistrationView, ListUsersAPIView, UpdateUserAPIView, get_departments, get_domains

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register-department'),
    path('users/', ListUsersAPIView.as_view(), name='list-users'),
    path('users/<int:id>/', UpdateUserAPIView.as_view(), name='update-user'),


    #FETCH ENDPOINTS
    path('departments/', get_departments, name='get-departments'),
    path('domains/', get_domains, name='get-domains'),


]
