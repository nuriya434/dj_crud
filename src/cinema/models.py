from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUser(AbstractBaseUser, UserManager):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class Hall(models.Model):
    name = models.CharField(max_length=255)

class Row(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    number = models.IntegerField()

class Seat(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    number = models.IntegerField()

class TicketType(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    seats_available = models.ManyToManyField(Seat)
    ticket_types = models.ManyToManyField(TicketType)

class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add=True)

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
