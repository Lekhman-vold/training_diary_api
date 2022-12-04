from django.urls import path

from .serializers import CustomObtainPairView
from apps.users.views import UpdateUser, Signup

urlpatterns = [
    path('signin/', CustomObtainPairView.as_view(), name='signin'),
    path('signup/', Signup.as_view(), name='signup'),
    path('<int:pk>', UpdateUser.as_view(), name='update_user'),
]
