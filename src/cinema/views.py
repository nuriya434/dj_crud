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
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')  # Перенаправление на главную страницу после успешного входа
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')


def save_user_data(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        Cinema.objects.create(name=username, address=password)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def cinema_list(request):
    api_url = 'https://example.com/api/cinemas/'
    response = requests.get(api_url)
    cinemas_data = response.json()

    for cinema_data in cinemas_data:
        cinema, created = Cinema.objects.get_or_create(
            name=cinema_data['name'],
            defaults={'location': cinema_data['location']}
        )

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

    search_query = request.GET.get('search')
    if search_query:
        movies = movies.filter(Q(title__icontains=search_query))

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

