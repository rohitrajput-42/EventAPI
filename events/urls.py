from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)  # User management
router.register(r'events', views.EventViewSet)  # Event management

urlpatterns = [
    path('register/', views.register, name='register'),
    path('events/<int:event_id>/purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Include other router URLs
]
