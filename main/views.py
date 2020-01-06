from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import GameRooms, Game
from .forms import *
import json

lastBoardState = [  ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,," \
                    ",,,,,,,,,,,,,,,"]


def homepage(request):
    return render(request, "main/home.html")


def game(request, gameroom_id):
    game_room = GameRooms.objects.get(pk=gameroom_id)
    if len(Game.objects.filter(game_room=game_room)) == game_room.seats:
        board_state = game_room.board_state
        print(board_state)
        return render(request, "main/viewgame.html", {"boardState" : board_state,
                                                     'gameroom_id_json': mark_safe(json.dumps(gameroom_id))})
    else:
        return render(request, "main/game.html", {"boardState": lastBoardState[0],
                                              'gameroom_id_json': mark_safe(json.dumps(gameroom_id))})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # domyślne uwierzytelnianie
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Zalogowano jako: {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Błędna nazwa użytkownika lub hasło")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Pomyślnie wylogowano")
    return redirect("main:homepage")


def register(request):
    if request.method == "POST":  # po wciśnięciu przycisku submit
        form = NewUserForm(request.POST)  # korzystamy z domyślnego formularza rejestracji nowego użytkownika
        if form.is_valid():
            user = form.save()  # tworzymy objekt, zapisujemy go w tabeli i jednocześnie przypisujemy do zmiennej user
            username = form.cleaned_data.get('username')  # przypisujemy zmiennej username wartość 'username' obiektu
            messages.success(request,
                             f"Zarejestrowano pomyślnie")  # wyświetlanie wiadomości; po kropce występuje tag wiadomości, dzięki czemu można rozróżniać ich rodzaje i np. dla różnych wiadomości wyświetlać komunikaty w różnej formie
            login(request, user)  # od razu po rejestrecji logujemy naszego użytkownika
            messages.info(request, f"Zalogowano jako: {username}")
            return redirect("main:homepage")  # przekierowanie do strony głównej
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm  # do zmiennej form przypisujemy domyślny formularz
    # w uproszczeniu render do danego requesta przypisuje url wraz z kontekstem (w tym wypadku, w register.html form będzie przypisany do zmiennej form
    return render(request, "main/register.html", context={"form": form})

def gameroom(request):
    return render(request,"main/gameroom.html",context = {"gamerooms": GameRooms.objects.all})

def gameroom_creator(request):
    if request.method == "POST":
        form = GameRoomCreatorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Błąd")
        return redirect("main:gameroom")
    else:
        form = GameRoomCreatorForm()
    return render(request, "main/gameroom_creator.html", context={"form": form})


def profile(request,user_id):
    user = User.objects.get(pk=user_id)
    played_games = Game.objects.filter(user=user).select_related('game_room__name')


    #jeszcze wyciągnij nazwy gier

    return render(request, "main/profile.html", context={'playedGames': played_games})