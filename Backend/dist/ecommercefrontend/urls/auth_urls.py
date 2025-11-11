# ecommercefrontend/urls/auth_urls.py

from django.urls import path
from ecommercefrontend.views.auth_views import SendOTPView, VerifyOTPView, HomeView, ProfileCompleteView 

urlpatterns = [
    # ✅ CORRECT: Using View classes (.as_view())
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    
    # Profile Completion
    path('profile-complete/', ProfileCompleteView.as_view(), name='profile_complete'),
    
    # Other Auth URLs (uncommented HomeView)
    path('home/', HomeView.as_view(), name='home'),
]