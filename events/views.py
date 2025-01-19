# events/views.py
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer, TicketSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = serializer.save()
            user.set_password(password)
            user.save()

            # Generate JWT tokens for the new user
            tokens = get_tokens_for_user(user)
            return Response({**serializer.data, 'tokens': tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User ViewSet (for listing and retrieving users)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only Admin can create users.")
        serializer.save()

# Event Management (Admin Only)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only Admin can create events.")
        serializer.save()

# Purchase Ticket (User Only)
@api_view(['POST'])
def purchase_ticket(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if event.tickets_sold + quantity > event.total_tickets:
        return Response({"error": "Not enough tickets available"}, status=status.HTTP_400_BAD_REQUEST)

    ticket = Ticket.objects.create(user=request.user, event=event, quantity=quantity)
    event.tickets_sold += quantity
    event.save()
    return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
