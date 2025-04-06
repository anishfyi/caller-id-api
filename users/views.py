from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    Creates a new user with profile information.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user and return the response with serialized data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.get_full_name(),
                'phone_number': str(user.profile.phone_number)  # Convert PhoneNumber to string
            }
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Get the current user's profile"""
        return self.request.user.profile
