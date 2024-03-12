from django.shortcuts import render
from .models import Movie, Session, Seat

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def session_detail(request, session_id):
    session = Session.objects.get(pk=session_id)
    seats = Seat.objects.filter(row__hall=session.hall)
    return render(request, 'session_detail.html', {'session': session, 'seats': seats})

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'session_list.html', {'sessions': sessions}) 



