from rest_framework import serializers
from .models import Seat, Session
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number']

class SessionSerializer(serializers.ModelSerializer):
    seats_available = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'movie', 'hall', 'date_time', 'seats_available', 'ticket_types']
