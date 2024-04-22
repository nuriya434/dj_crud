import requests
from .models import Cinema

def fetch_and_save_cinemas():
    api_url = 'https://example.com/api/cinemas/'
    response = requests.get(api_url)
    cinemas_data = response.json()

    for cinema_data in cinemas_data:
        cinema, created = Cinema.objects.get_or_create(
            name=cinema_data['name'],
            address=cinema_data['address']
        )
        cinema.latitude = cinema_data.get('latitude', None)
        cinema.longitude = cinema_data.get('longitude', None)
        cinema.save()