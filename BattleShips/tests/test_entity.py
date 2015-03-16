import unittest

from BattleShips.tests import BattleShipsTest
from BattleShips.entity import GameBoard, BattleField, Fleet, Ship


class TestEntity(BattleShipsTest):
    def setUp(self):
        pass

    # BattleField tests

    def test_position_fleet(self):
        for i in range(0, 100):  # running the test 100 times
            battle_field = BattleField(10, 10)
            self.position_fleet_test(battle_field)

    def test_only_horizontal_ship_positioning(self):
        # for i in range(0, 10):  # running the test 10 times
        for i in range(0, 10):  # running the test 10 times
            battle_field = BattleField(3, 10)  # Min ship length is 4 so 3 will force other positioning
            self.position_fleet_test(battle_field)
            self.ship_orientation_test(battle_field, BattleField.HORIZONTAL)

    def test_only_vertical_ship_positioning(self):
        for i in range(0, 10):  # running the test 10 times
            battle_field = BattleField(10, 3)  # Min ship length is 4 so 3 will force other positioning
            self.position_fleet_test(battle_field)
            self.ship_orientation_test(battle_field, BattleField.VERTICAL)

    def position_fleet_test(self, battle_field):
        description = (
            (Ship.destroyer, 2),
            (Ship.fighter, 1)
        )
        fleet = Fleet('testing_fleet', description)

        battle_field.position_fleet(fleet)

        fleets = battle_field.get_positioned_fleets()
        ship_parts = {}
        for fleet in fleets:
            fleet_ships = fleet.get_ships()
            for group_name in fleet_ships:
                ships_list = fleet_ships[group_name]
                for ship in ships_list:
                    self.assertEquals(True, ship.is_positioned(), "Ship {} not positioned".format(ship))
                    for ship_part in ship.get_position():
                        if ship_part in ship_parts:
                            raise AssertionError('Ship {} crosses ship {}'.format(ship, ship_parts[ship_part]))
                        else:
                            ship_parts[ship_part] = ship

    def ship_orientation_test(self, battle_field, orientation):
        fleets = battle_field.get_positioned_fleets()
        for fleet in fleets:
            fleet_ships = fleet.get_ships()
            for group_name in fleet_ships:
                ships_list = fleet_ships[group_name]
                for ship in ships_list:
                    self.assertEquals(orientation, ship.get_orientation())

    # Fleet tests

    def test_fleet_creation(self):
        description = (
            (Ship.destroyer, 2),
            (Ship.fighter, 1)
        )
        fleet = Fleet('testing_fleet', description)

        fleet_ships = fleet.get_ships()

        self.assertEquals(2, len(fleet_ships['Destroyer']))
        self.assertEquals(1, len(fleet_ships['Fighter']))

    # GameBoard tests

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
