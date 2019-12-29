from channels.generic.websocket import WebsocketConsumer
from .models import Move, GameRooms
import json


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        board_state = text_data_json['boardState']
        points = text_data_json['points']
        player = text_data_json['player']
        gameroom = text_data_json['gameroom']
        game_room = GameRooms.objects.get(pk = gameroom)
        game_room.Move.create(player = player, points = points, board_state = board_state)
        # tutaj trzeba zrobić jakieś casy w zależności od tego, czy wszyscy zrobili ruch, czy nie, bo nie wyobrażam sobie tego inaczej
        # trzeba by chyba też jakiś mechanizm dołączania do gry zrobić i wtedy by się ten model Game nadał
        self.send(text_data=json.dumps({
            'boardState': board_state
        }))