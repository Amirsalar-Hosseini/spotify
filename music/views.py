from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests


def top_artists():
    url = "" # url top artists from api music website storage (for example rapidapi.com/top-artists)
    headers = {
        "<this for api key>": "", # api
        "<this for api host>": "" # EX: spotify-scraper.p.rapidapi.com
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    artists_info = []

    if 'artists' in response_data:
        for artist in response_data['artists']:
            name = artist.get('name', 'No Name')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))

    return artists_info

def top_tracks():
    url = "" # url top artists from api music website storage (for example rapidapi.com/top-artists)
    headers = {
        "<this for api key>": "", # api
        "<this for api host>": "" # EX: spotify-scraper.p.rapidapi.com
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    track_details = []
    if 'tracks' in data:
        shortened_data = data['tracks'][:18]
        # id, name, artist_name, cover url
        for track in shortened_data:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['cover'][0]['url'] if track['album']['cover'] else None

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url,
            })
    else:
        print('No tracks found')
    return track_details


@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    top_track_list = top_tracks()

    # 18 / 6 = 3 parts
    first_six_tracks = top_track_list[:6]
    second_six_tracks = top_track_list[6:12]
    third_six_tracks = top_track_list[12:18]

    context = {
        'artists_info': artists_info,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }
    return render(request, 'index.html', context=context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already registered.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login_user = auth.authenticate(username=username, password=password)
                auth.login(request, login_user)
                messages.info(request, 'User created successfully.')
                return redirect('index')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')