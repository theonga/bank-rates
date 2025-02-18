from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, RegisterView, CustomTokenObtainPairView, UserProfileView, BankUsersView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', ProfileViewSet)

urlpatterns = [
    path('', UserProfileView.as_view(), name='user_profile'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bank-users/<int:bank_id>', BankUsersView.as_view(), name='bank_users'),
]