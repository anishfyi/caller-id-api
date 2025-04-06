from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from phonenumber_field.serializerfields import PhoneNumberField

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    Handles phone number display and validation.
    """
    phone_number = PhoneNumberField()

    class Meta:
        model = UserProfile
        fields = ('phone_number',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation with profile information.
    """
    phone_number = PhoneNumberField()
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name', 'phone_number')
        extra_kwargs = {'email': {'required': False}}

    def validate_phone_number(self, value):
        """
        Validate that the phone number is not already registered.
        """
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        """
        Create a new user with profile information.
        """
        name = validated_data.pop('name')
        phone_number = validated_data.pop('phone_number')
        
        # Split name into first_name and last_name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        # Update profile
        user.profile.phone_number = phone_number
        user.profile.save()

        return user 