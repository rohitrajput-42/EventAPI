from django.contrib.auth.models import AbstractUser
from django.db import models

#A custom User model with Roles added
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        USER = 'User'

    #User groups
    role = models.CharField(max_length=10, choices=Role.choices)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='event_users',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups')
    )
    #User permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='event_users',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions')
    )

    def __str__(self):
        return self.username

#Model for Event
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_tickets = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name

#Model for Ticket
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #The users that are purchasing the ticket
    event = models.ForeignKey(Event, on_delete=models.CASCADE) #The events for which the ticket have been purachased
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} tickets for {self.event.name} by {self.user.username}"
