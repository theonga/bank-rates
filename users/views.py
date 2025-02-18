from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class BankUsersView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        bank_id = self.kwargs['bank_id']
        return Profile.objects.filter(bank_id=bank_id)