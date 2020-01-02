from django.contrib import admin
from .models import GameRooms, Move, Game

admin.site.register(GameRooms)
admin.site.register(Move)
admin.site.register(Game)