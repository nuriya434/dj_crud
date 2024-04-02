from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Session, Seat
from django.http import JsonResponse
from .forms import MovieForm
from .filters import MovieFilter
from django_filters.views import FilterView
from rest_framework import generics
from .serializers import SessionSerializer

class SessionList(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

class MovieFilterView(FilterView):
    filterset_class = MovieFilter
    queryset = Movie.objects.all()
    template_name = 'movie_list.html'

def movie_manage(request):
    movies = Movie.objects.all()
    return render(request, 'movie_manage.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list') 
    else:
        form = MovieForm()
    return render(request, 'create_movie.html', {'form': form})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.delete()
    return JsonResponse({'success': True})

def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'update_movie.html', {'form': form, 'movie': movie})
def session_detail(request, session_id):
    session = Session.objects.get(pk=session_id)
    seats = Seat.objects.filter(row__hall=session.hall)
    return render(request, 'session_detail.html', {'session': session, 'seats': seats})

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'session_list.html', {'sessions': sessions})