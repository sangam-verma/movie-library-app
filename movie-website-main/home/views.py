from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import re
from .models import Movie, Playlist

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if first_name and email and password1 and password2:
            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "This email is already taken")
                    return redirect("/register")

                else:
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if(re.fullmatch(regex, email)):
                        user = User.objects.create_user(username=email, password=password1, first_name=first_name, email=email)
                        user.save()
                        playlist = Playlist.objects.create(user_id=user.id)
                        playlist.save()
                        messages.info(request, "Account created successfully! Login to continue!")
                        return redirect("/login")
                
                    else:
                        messages.info(request, "Please enter a valid email")
                        return redirect("/register")

            else:
                messages.info(request, "Passwords dont match")
                return redirect("/register")

        else:
            messages.info(request, "Please enter all the fields")
            return redirect("/register")

    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            messages.info(request, "Please enter a valid email")
            return redirect("/login")

        if User.objects.filter(email=email).exists():
            arpan = User.objects.get(email=email)
            
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
        
        user = auth.authenticate(username=arpan.username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login successfully')
            return redirect('/')

    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def index(request):
    if request.user.is_authenticated:
        movies = Movie.objects.filter(user_id=request.user.id)
        playlist = Playlist.objects.get(user_id=request.user.id)
        return render(request, "index.html", {"movies": movies, "playlist": playlist})

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")

def details(request, id):
    if request.user.is_authenticated:
        return render(request, "details.html", {"id": id})

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")


def details_saved(request, idd, id):
    if request.user.is_authenticated:
        return render(request, "details_saved.html", {"id": id, "idd": idd})

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")

def save_details(request):
    if request.user.is_authenticated:
        id = request.GET['id']
        poster = request.GET['poster']
        year = request.GET['year']
        title = request.GET['title']

        if id and poster and year and title:
            if poster == "N/A":
                poster = None
            
            movie = Movie.objects.create(title=title, poster=poster, year=year, imdbid=id, user_id=request.user.id)
            movie.save()
            
        return redirect("/")

        return render(request, "details.html", {"id": id})

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")


def delete(request, id):
    if request.user.is_authenticated:
        if Movie.objects.filter(id=id).exists():
            movie = Movie.objects.get(id=id)
            movie.delete()
            return redirect("/")

        else:
            return redirect("/")

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")
    
def make_public_playlist(request):
    if request.user.is_authenticated:
        playlist = Playlist.objects.get(user_id=request.user.id)
        playlist.public = True
        playlist.save()
        return redirect("/")

    else:
        messages.info(request, "Login to continue")
        return redirect("/login")    
        
def make_private_playlist(request):
    if request.user.is_authenticated:
        playlist = Playlist.objects.get(user_id=request.user.id)
        playlist.public = False
        playlist.save()
        return redirect("/")

    else:
        messages.info(request, "Login to continue")
        return redirect("/login") 

def public_playlist(request, id):
    if Playlist.objects.filter(user_id=id).exists():
        playlist = Playlist.objects.get(user_id=id)

        if playlist.public:
            movies = Movie.objects.filter(user_id=id)

        else:
            movies = None

        return render(request, "public_playlist.html", {"movies": movies, "playlist": playlist})
            

    else:
        return redirect("/") 
