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
        self.room_name = self.scope['url_route']['kwargs']['gameroom_name']
        temp = GameRooms.objects.get(pk=self.room_name)
        temp.in_progress = False
        temp.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        board_state = text_data_json['boardState']
        gameroom = text_data_json['gameroom']
        round = text_data_json['round']
        if board_state == "LETTERS":
            letters_remaining = text_data_json['lettersRemaining']
            letters_given = text_data_json['lettersGiven']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'letters_info',
                    'boardState': 'LETTERS',
                    'lettersRemaining': letters_remaining,
                    'lettersGiven': letters_given
                }
            )
        else:
            player = text_data_json['player']
            game_room = GameRooms.objects.get(pk=gameroom)
            if board_state == 'READY':

                user = User.objects.get(username=player)
                Game.objects.create(game_room=game_room,user=user)
                self.send(text_data=json.dumps({
                    'boardState': 'WAITING_FOR_START'
                }))

                if len(Game.objects.filter(game_room=game_room)) == game_room.seats:
                    temp = GameRooms.objects.get(pk=gameroom)
                    temp.in_progress = True
                    temp.save()
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'start_info',
                            'boardState': 'START',
                            'round': (round + 1)
                        }
                    )
            else:
                points = text_data_json['points']
                Move.objects.create(game_room=game_room, player=player, points=points, board_state=board_state, round=round)
                # tutaj trzeba zrobić jakieś casy w zależności od tego, czy wszyscy zrobili ruch, czy nie, bo nie wyobrażam sobie tego inaczej
                # trzeba by chyba też jakiś mechanizm dołączania do gry zrobić i wtedy by się ten model Game nadał
                self.send(text_data=json.dumps({
                    'boardState': 'NOT YET',
                    'points': points
                }))
                moves = Move.objects.filter(game_room=game_room, round=round)
                if len(moves) == game_room.seats:
                    winner = moves.order_by('points').last()
                    board_state = winner.board_state
                    round_winner = winner.player
                    temp = Game.objects.get(user=User.objects.get(username=round_winner))
                    points = temp.points = temp.points + winner.points
                    temp.save()

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'move_info',
                            'boardState': board_state,
                            'round': (round+1),
                            'Winner': round_winner,
                            'points': points
                        }
                    )

    def move_info(self, event):
        board_state = event['boardState']
        round = event['round']
        round_winner = event['Winner']
        points = event['points']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'boardState': board_state,
            'round': round,
            'Winner': round_winner,
            'points': points
        }))

    def start_info(self, event):
        board_state = event['boardState']
        round = event['round']
        self.send(text_data=json.dumps({
            'boardState': board_state,
            'round': round
        }))

    def letters_info(self, event):
        board_state = event['boardState']
        letters_remaining = event['lettersRemaining']
        letters_given = event['lettersGiven']
        self.send(text_data=json.dumps({
            'boardState': board_state,
            'lettersRemaining': letters_remaining,
            'lettersGiven': letters_given
        }))