from rest_framework import serializers
from .models import Seat, Session

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number']

class SessionSerializer(serializers.ModelSerializer):
    seats_available = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'movie', 'hall', 'date_time', 'seats_available', 'ticket_types']
