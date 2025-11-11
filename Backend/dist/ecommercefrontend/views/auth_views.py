# ecommercefrontend/views/auth_views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
# THE FIX IS HERE: Using ProfileCompleteSerializer
from ..serializers.auth_serializers import SendOTPSerializer, VerifyOTPSerializer, ProfileCompleteSerializer
import random 

# ---------- 1. Send OTP View ----------
class SendOTPView(generics.GenericAPIView):
    serializer_class = SendOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # Get or Create the user for OTP login
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            # Set a temporary username (optional, but AbstractUser needs one)
            user.username = phone 
            user.set_unusable_password() # Ensure they can't log in with a password
            user.save()

        # 4 digit OTP generation
        otp = str(random.randint(1000, 9999)) 
        user.otp = otp
        user.save()

        print(f"OTP for {phone}: {otp}") 

        return Response({"message": "OTP sent successfully!", "phone": phone}, status=status.HTTP_200_OK)


## ---------- 2. Verify OTP and Login View ----------
class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        
        user = serializer.validated_data 

        # Clear OTP and generate tokens
        user.otp = None 
        user.save()
        
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": f"Welcome {user.phone}",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_profile_complete": user.is_profile_complete
        }, status=status.HTTP_200_OK)


# ---------- 3. Home View (Check Auth) ----------
class HomeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            "message": f"Welcome {user.phone} to Home Page!",
            "is_profile_complete": user.is_profile_complete,
            "note": "You can view products, Buy now, or manage cart."
        })

# ---------- 4. Profile Completion View ----------
class ProfileCompleteView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileCompleteSerializer 
    
    def get_object(self):
        return self.request.user 

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Profile updated successfully!"})