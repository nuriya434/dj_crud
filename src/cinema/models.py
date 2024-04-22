# В файле models.py вашего приложения cinema
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

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
