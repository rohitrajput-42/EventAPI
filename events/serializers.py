from rest_framework import serializers
from .models import User, Event, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    tickets_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'total_tickets', 'tickets_sold', 'tickets_remaining']

    def get_tickets_remaining(self, obj):
        return obj.total_tickets - obj.tickets_sold

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'event', 'quantity', 'purchase_date']
