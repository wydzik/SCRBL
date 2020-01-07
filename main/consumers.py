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
        temp.finished = True
        temp.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'disconnect_info',
                'boardState': 'DISCONNECT',
            }
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
                    self.send(text_data=json.dumps({
                        'boardState': 'LETTERS_PROVIDER'
                    }))
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
                word_list = text_data_json['wordList']
                print(word_list)
                if type(word_list) == str:
                    first_letter = word_list[0].lower()
                    print(word_list)
                    letter_dictionary = open("./static/slowniki/" + first_letter + ".txt", "r")
                    dictionary_words = letter_dictionary.readlines()
                    if word_list.lower() + '\n' not in dictionary_words:
                        points = 0
                    letter_dictionary.close()
                else:
                    guard = len(word_list)
                    for word in word_list:
                        first_letter = word[0].lower()
                        print(word)
                        letter_dictionary = open("./static/slowniki/" + first_letter + ".txt", "r")
                        dictionary_words = letter_dictionary.readlines()
                        if word.lower() + '\n' in dictionary_words:
                            guard = guard - 1
                        letter_dictionary.close()

                    if guard != 0:
                        points = 0
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
                    if winner.points == 0:
                        game_winner = Game.objects.filter(game_room=game_room)
                        game_winner = game_winner.order_by('points').last()
                        game_winner_name = game_winner.user.username
                        game_winner_points = game_winner.points
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'winner_info',
                                'boardState': 'WINNER',
                                'round': (round + 1),
                                'winner': game_winner_name,
                                'points': game_winner_points,
                            }
                        )
                    else:
                        board_state = winner.board_state
                        game_room.board_state = board_state
                        game_room.save()
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
                                'points': points,
                                'winnerPoints': winner.points
                            }
                        )

    def move_info(self, event):
        board_state = event['boardState']
        round = event['round']
        round_winner = event['Winner']
        points = event['points']
        winner_points = event['winnerPoints']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'boardState': board_state,
            'round': round,
            'Winner': round_winner,
            'points': points,
            'winnerPoints': winner_points
        }))

    def winner_info(self, event):
        board_state = event['boardState']
        round = event['round']
        game_winner = event['winner']
        points = event['points']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'boardState': board_state,
            'round': round,
            'winner': game_winner,
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