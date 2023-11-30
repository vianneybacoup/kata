#!/usr/bin/env python

class Logger:
    def log(self, str):
        print(str)


class Game:

    def __init__(self):
        self.logger = Logger()
        self.players = []
        self.places = []
        self.purses = []
        self.in_penalty_box = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False
        
        self.questions = {
            "Pop": [],
            "Science": [],
            "Sports": [],
            "Rock": []
        }
        for questionType in self.questions:
            self.init_question(questionType)
    
    def init_question(self, questionType):
        self.questions[questionType] = []
        for i in range(50):
            self.questions[questionType].append(questionType + str(i))

    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def is_playable(self):
        return self.how_many_players >= 2 and self.how_many_players <= 6

    def add(self, player_name):
        if (self._has_maximum_players()):
            raise Exception("Maximum players reached")

        self.players.append(player_name)

        self.places.append(0)
        self.purses.append(0)
        self.in_penalty_box.append(False)

        self.logger.log(player_name + " was added")
        self.logger.log("They are player number %s" % len(self.players))

        return True

    def _has_maximum_players(self):
        return self.how_many_players >= 6

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self.logger.log("%s is the current player" % self.players[self.current_player])
        self.logger.log("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                self.logger.log("%s is getting out of the penalty box" % self.players[self.current_player])
                self._update_position(roll)

                self.logger.log(self.players[self.current_player] +
                            '\'s new location is ' +
                            str(self.places[self.current_player]))
                self.logger.log("The category is %s" % self._current_category)
                self._ask_question()
            else:
                self.logger.log("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self._update_position(roll)

            self.logger.log(self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player]))
            self.logger.log("The category is %s" % self._current_category)
            self._ask_question()

    def _update_position(self, roll):
        self.places[self.current_player] = (self.places[self.current_player] + roll) % 12
        

    def _ask_question(self):
        if (len(self.questions[self._current_category]) == 0):
            self.init_question(self._current_category)
        self.logger.log(self.questions[self._current_category].pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] % 4 == 0: return 'Pop'
        if self.places[self.current_player] % 4 == 1: return 'Science'
        if self.places[self.current_player] % 4 == 2: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                self.in_penalty_box[self.current_player] = False
                self.logger.log('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                self.logger.log(
                    self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.'
                )

                winner = self._did_player_win()
                self._next_player()

                return winner
            else:
                self._next_player()
                return True
        else:
            self.logger.log("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            self.logger.log(self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self._next_player()

            return winner

    def _next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def wrong_answer(self):
        self.logger.log('Question was incorrectly answered')
        self.logger.log(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self._next_player()
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)


from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break