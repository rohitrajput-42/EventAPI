from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer, TicketSerializer

#View code for new user registration
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] #This defines that any user could register

    #Saving the user with additional access parameters, such as(staff and superuser access)
    def perform_create(self, serializer):
        user = serializer.save()
        if user.role == 'Admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

#VIew code for event creation
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser] #This defines that users with Admin role can assess this api
        else:
            self.permission_classes = [permissions.AllowAny] #This defines that users with any role(Admin, user) can assess this api
        return super().get_permissions()

#VIew code for purchasing ticket
class TicketPurchaseView(generics.GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        #Logic to check if only users with User role can purchase ticket
        if request.user.role != 'User':
            return Response({"error": "Only users with the User role can purchase tickets."}, status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        #Logic to check if quantity of tickets are greater than 0
        quantity = request.data.get('quantity')
        if int(quantity) <= 0:
            return Response({"error": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        if event.tickets_sold + int(quantity) > event.total_tickets:
            return Response({"error": "Not enough tickets available."}, status=status.HTTP_400_BAD_REQUEST)

        #Logic to update the ticket sold and also add a new entry in ticket table
        event.tickets_sold += int(quantity)
        event.save()

        ticket = Ticket.objects.create(
            user=request.user,
            event=event,
            quantity=quantity
        )
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)

#VIew code for viewing Users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] #This defines that users with Admin role can assess this api

#VIew code for viewing events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny] #This defines that users with any role(Admin, user) can assess this api

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No events to show."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)