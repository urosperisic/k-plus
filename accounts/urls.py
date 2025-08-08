from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    logout_view,
    delete_user,
    UserListView,
    UpdateUserRoleView,
)

from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', logout_view, name='logout'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('update-role/<int:user_id>/', UpdateUserRoleView.as_view(), name='update_user_role'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
