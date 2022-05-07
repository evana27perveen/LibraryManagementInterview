from django.urls import path
from App_auth import views

# API login imports
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

app_name = 'App_auth'

urlpatterns = [
    path('registerAPI/', views.RegisterAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
