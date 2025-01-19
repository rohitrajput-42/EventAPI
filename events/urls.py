from django.urls import path
from .views import RegisterUserView, EventListCreateView, TicketPurchaseView, UserListView, EventListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('view_events/', EventListView.as_view(), name='event-list'),
]
