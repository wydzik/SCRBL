from django.contrib import admin
from .models import GameRooms, Move, Profile

admin.site.register(GameRooms)
admin.site.register(Move)
admin.sites.register(Profile)
