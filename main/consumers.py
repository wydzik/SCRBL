from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import Move, GameRooms, Game
import json


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['gameroom_name']
        self.room_group_name = 'game_%s' % self.room_name


        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        board_state = text_data_json['boardState']
        player = text_data_json['player']
        gameroom = text_data_json['gameroom']
        game_room = GameRooms.objects.get(pk=gameroom)
        if board_state == 'READY':
            user = User.objects.get(username=player)
            Game.objects.create(game_room=game_room,user=user)
            self.send(text_data=json.dumps({
                'boardState': 'WAITING_FOR_START'
            }))
        else:
            points = text_data_json['points']
            Move.objects.create(game_room=game_room, player=player, points=points, board_state=board_state)
            # tutaj trzeba zrobić jakieś casy w zależności od tego, czy wszyscy zrobili ruch, czy nie, bo nie wyobrażam sobie tego inaczej
            # trzeba by chyba też jakiś mechanizm dołączania do gry zrobić i wtedy by się ten model Game nadał
            self.send(text_data=json.dumps({
                'boardState': 'NOT YET',
                'points': points
            }))
            if len(Move.objects.filter(game_room=game_room)) == 2 :

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'move_info',
                        'boardState': board_state
                    }
                )

    def move_info(self, event):
        board_state = event['boardState']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'boardState': board_state
        }))

        # self.send(text_data=json.dumps({
        #     'boardState': board_state,
        #     'points': points
        # }))
