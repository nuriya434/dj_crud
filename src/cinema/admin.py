# admin.py
from django.contrib import admin
from .models import Movie, Hall, Row, Seat, Ticket, TicketType, Session, Cinema, CustomUser

admin.site.register(Movie)
admin.site.register(Hall)
admin.site.register(Row)
admin.site.register(Seat)
admin.site.register(TicketType)
admin.site.register(Session)
admin.site.register(Ticket)
admin.site.register(CustomUser)

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  
    search_fields = ('name', 'address')
