from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .froms import *
import random


def homepage(request):
    return render(request, "main/home.html")


def game(request):
    letters = [
        'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', chr(260),
        'B', 'B', 'C', 'C', 'C', chr(262), 'D', 'D', 'D', 'E',
        'E', 'E', 'E', 'E', 'E', 'E', chr(280), 'F', 'G', 'G',
        'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
        'J', 'J', 'K', 'K', 'K', 'L', 'L', 'L', chr(321), chr(321),
        'M', 'M', 'M', 'N', 'N', 'N', 'N', 'N', chr(323), 'O',
        'O', 'O', 'O', 'O', 'O', chr(211), 'P', 'P', 'P', 'R',
        'R', 'R', 'R', 'S', 'S', 'S', 'S', chr(346), 'T', 'T',
        'T', 'U', 'U', 'W', 'W', 'W', 'W', 'Y', 'Y', 'Y',
        'Y', 'Z', 'Z', 'Z', 'Z', 'Z', chr(377), chr(379), '_', '_'
    ]
    chosen = []
    taken = []
    while len(chosen) < 7:
        temp = random.randint(0, 99)
        if temp not in taken:
            chosen.append(letters[temp])
            taken.append(temp)

    return render(request, "main/game.html", {"letters": chosen})


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
