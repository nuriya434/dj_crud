# cinema/urls.py
from django.urls import path
from .views import movie_list, session_list, session_detail

urlpatterns = [
    path('', movie_list, name='home'),
    path('movies/', movie_list, name='movie_list'),
    path('sessions/', session_list, name='session_list'),
    path('session/<int:session_id>/', session_detail, name='session_detail'),
]
