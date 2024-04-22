from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Session, Seat, Cinema
from django.http import JsonResponse
from .forms import MovieForm
from .filters import MovieFilter
from .serializers import SessionSerializer
from django.db.models import Q
import requests
from rest_framework import generics
from django_filters.views import FilterView



def save_user_data(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Создаем новую запись в базе данных
        Cinema.objects.create(name=username, address=password)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def cinema_list(request):
    # Получаем данные о кинотеатрах из стороннего API
    api_url = 'https://example.com/api/cinemas/'
    response = requests.get(api_url)
    cinemas_data = response.json()

    # Создаем или обновляем записи в базе данных на основе полученных данных
    for cinema_data in cinemas_data:
        cinema, created = Cinema.objects.get_or_create(
            name=cinema_data['name'],
            defaults={'location': cinema_data['location']}
        )

    # Получаем список кинотеатров из базы данных
    cinemas = Cinema.objects.all()

    return render(request, 'cinema_list.html', {'cinemas': cinemas})

class SessionList(generics.ListAPIView):
    queryset = Session.objects.prefetch_related('seats_available').all()
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

    # Обработка поискового запроса
    search_query = request.GET.get('search')
    if search_query:
        movies = movies.filter(Q(title__icontains=search_query))

    # Обработка сортировки
    sort_by = request.GET.get('sort')
    if sort_by == 'title':
        movies = movies.order_by('title')

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

