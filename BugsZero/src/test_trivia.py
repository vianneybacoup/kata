import unittest

from trivia import Game

def create_game_with_n_players(game: Game, n):
    for i in range(n):
        game.add("foo" + str(i))
    return game

def odd_roll(game):
    game.roll(1)

def next_player_roll_even(game):
    game.roll(2)


class GameMock(Game):
    asked_question_called_count = 0

    def _ask_question(self):
        self.asked_question_called_count += 1


class TrivaTest(unittest.TestCase):
    def test_when_less_than_two_players_game_should_not_be_playable(self):
        game = create_game_with_n_players(Game(), 1)
        self.assertFalse(game.is_playable())

    def test_when_min_two_players_and_max_six_players_game_should_be_playable(self):
        for i in range(2, 7):
            game = create_game_with_n_players(Game(), i)
            self.assertTrue(game.is_playable(), str(i) + " is failing")
        
    def test_when_more_than_six_players_game_should_not_be_playable(self):
        with self.assertRaises(Exception):
             create_game_with_n_players(Game(), 7)

    def test_when_rolling_a_dice_while_player_is_on_last_box(self):
        game = create_game_with_n_players(Game(), 1)
        game.places[0] = 11
        game.roll(1)
        self.assertEqual(0, game.places[0])

    def test_when_wrong_answer_player_should_be_in_penalty_box(self):
        game = create_game_with_n_players(Game(), 1)
        game.wrong_answer()
        self.assertTrue(game.in_penalty_box[0])

    def test_when_in_penalty_box_and_roll_odd_and_correct_answer_should_be_out(self):
        game = create_game_with_n_players(Game(), 1)
        game.in_penalty_box[0] = True

        odd_roll(game)
        game.was_correctly_answered()
        self.assertFalse(game.in_penalty_box[0])
        
    def test_when_in_penalty_box_and_roll_even_no_question_asked(self):
        game = create_game_with_n_players(GameMock(), 1)
        game.in_penalty_box[0] = True

        next_player_roll_even(game)
        self.assertEqual(game.asked_question_called_count, 0)


if __name__ == '__main__':
    unittest.main()


# A game must have at least 2 players
# A game must have no more than 6 players
# A game have a board of 12 boxes
# It is a turn based game

# Each player have a bag of coins
# Each player have a location on the board, between 0 and 11
# A player should be able to roll a dice at his/her turn
# After rolling a dice, a player should move forward the number of steps of the dice
# and should answer a question
# if a player is in the last box, he/she should go back to the first box
# A player should go in penalty box if he/she answers a question wrong
# When a player in penalty box, at his turn he must roll a dice, if the value
# is odd, he/she will go out of penalty box and will be able to move forward