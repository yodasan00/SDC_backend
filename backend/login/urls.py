from django.urls import path
from .views import  LoginAPIView, RegistrationView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register-department'),

]
