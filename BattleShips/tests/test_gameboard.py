import unittest

from BattleShips.tests.battleships_test import BattleShipsTest
from BattleShips.entity import GameBoard


class TestGameBoard(BattleShipsTest):

    def setUp(self):
        pass

    def test_rols_and_cols(self):
        game_board = GameBoard(10, 10)
        self.assertEquals(10, game_board.get_rows())
        self.assertEquals(10, game_board.get_cols())

    def test_rows_shouldnt_be_more_than_letters(self):

        exception_raised = True
        try:
            GameBoard(27, 10)
            exception_raised = False
        except Exception as ex:
            self.assertMatch('rows exceeded', ex[0])

        self.assertEquals(True, exception_raised, 'Expected exception not raised')

    def test_board_positions(self):
        letters_map = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'
        }

        game_board = GameBoard(5, 5)
        self.assertEquals(('A', 'B', 'C', 'D', 'E'), game_board.get_rows_letters())
        self.assertEquals(letters_map, game_board.get_letters_map())


if __name__ == '__main__':
    unittest.main()

