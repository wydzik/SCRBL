from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class GameRooms(models.Model):
    name = models.CharField(max_length=250, default="Too lazy to name")
    in_progress = models.BooleanField(default=False)
    board_state = models.CharField(max_length=450, default=",,,,,,,,,,,,,,," \
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
                                                           ",,,,,,,,,,,,,,,")
    seats = models.IntegerField(default=2)
    finished = models.BooleanField(default=False)
class Game(models.Model):
    game_room = models.ForeignKey(GameRooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Move(models.Model):
    game_room = models.ForeignKey(GameRooms, on_delete=models.CASCADE)
    player = models.CharField(max_length= 500, default=None)
    board_state = models.CharField(max_length=450, default=",,,,,,,,,,,,,,," \
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
                                                           ",,,,,,,,,,,,,,,")
    points = models.IntegerField(default=0)
    round = models.IntegerField(default=0)
    # points trzeba liczyć po stronie usera, bo on ma te pdwójne, potrójne pola i najwyżej zerować jak nie ma w słowniku i tyle
