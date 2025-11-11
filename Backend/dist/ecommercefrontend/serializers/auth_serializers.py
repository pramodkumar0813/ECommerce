# ecommercefrontend/serializers/auth_serializers.py
from rest_framework import serializers
from ..models import User

# ---------- 1. Send OTP Serializer (Register or Login) ----------
class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

# ---------- 2. Verify OTP Serializer ----------
class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number.")

        if not user.otp or user.otp != otp:
             raise serializers.ValidationError("Invalid or expired OTP.")
        
        return user 

# ---------- 🆕 3. Complete Profile/Sign-up Serializer ----------
class ProfileCompleteSerializer(serializers.ModelSerializer):
    # Full Name fields are inherited from AbstractUser (first_name, last_name)
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 
            'address_line_1', 'street_name', 'city', 'state', 'pincode'
        ]
        extra_kwargs = {
            'email': {'required': False}, # Email is optional
        }

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists() and self.instance and self.instance.email != value:
            raise serializers.ValidationError("This email is already registered.")
        return value

    def update(self, instance, validated_data):
        # Profile fields update
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.address_line_1 = validated_data.get('address_line_1', instance.address_line_1)
        instance.street_name = validated_data.get('street_name', instance.street_name)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        
        # Address fileds all filled it gives true
        if (instance.address_line_1 and instance.street_name and 
            instance.city and instance.state and instance.pincode and instance.first_name):
            instance.is_profile_complete = True
        
        instance.save()
        return instance