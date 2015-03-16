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
            battle_field = BattleField(3, 5)  # Min ship length is 4 so 3 will force other positioning
            self.position_fleet_test(battle_field)
            self.ship_orientation_test(battle_field, BattleField.HORIZONTAL)

    def test_only_vertical_ship_positioning(self):
        for i in range(0, 10):  # running the test 10 times
            battle_field = BattleField(5, 3)  # Min ship length is 4 so 3 will force other positioning
            self.position_fleet_test(battle_field)
            self.ship_orientation_test(battle_field, BattleField.VERTICAL)

    def test_not_enough_field(self):
        for i in range(0, 10):  # running the test 10 times
            battle_field = BattleField(3, 4)  # Not enough space for the fleet

            exception_raised = True
            try:
                self.position_fleet_test(battle_field)
                exception_raised = False
            except Exception as ex:
                self.assertMatch("Can't place fleet ships. Too much ships on a small field.", ex[0])

            self.assertEquals(True, exception_raised, 'Expected exception not raised')

    def test_add_shot(self):
        battle_field = BattleField(5, 5)
        fleet = Fleet('test_fleet', ((Ship.DESTROYER, 1),))

        battle_field.position_fleet(fleet)
        fleets = battle_field.get_positioned_fleets()
        ship = None

        for fleet in fleets:
            fleet_ships = fleet.get_ships()
            for group_name in fleet_ships:
                ships_list = fleet_ships[group_name]
                for current_ship in ships_list:
                    ship = current_ship
                    break

        if isinstance(ship, Ship):
            import random
            ship_position = ship.get_position()
            print ship_position

            ship_part = None
            non_ship_part = None

            while True:
                i = random.randint(0, 4)
                j = random.randint(0, 4)

                if (i, j) not in ship_position and not isinstance(non_ship_part, tuple):
                    non_ship_part = (i, j)
                elif (i, j) in ship_position and not isinstance(ship_part, tuple):
                    ship_part = (i, j)

                if isinstance(ship_part, tuple) and isinstance(non_ship_part, tuple):
                    break

            self.assertEquals(battle_field.add_shot(ship_part), ship)
            self.assertEquals(battle_field.add_shot(non_ship_part), BattleField.RESULT_MISS)
            self.assertEquals(battle_field.get_shots_count(), 2)
        else:
            raise AssertionError("Expected ship is not a Ship")

    def position_fleet_test(self, battle_field):
        description = (
            (Ship.DESTROYER, 2),
            (Ship.FIGHTER, 1)
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
            (Ship.DESTROYER, 2),
            (Ship.FIGHTER, 1)
        )
        fleet = Fleet('testing_fleet', description)

        fleet_ships = fleet.get_ships()

        self.assertEquals(2, len(fleet_ships['Destroyer']))
        self.assertEquals(1, len(fleet_ships['Fighter']))

        exception_raised = True
        try:
            description = "incorrect"
            Fleet('testing_fleet', description)
            exception_raised = False
        except Exception as ex:
            self.assertMatch('Fleet description must be tuple', ex[0])

        self.assertEquals(True, exception_raised, 'Expected exception not raised')

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

    # Ship tests

    def test_ship_positioning(self):
        from BattleShips.factory import ShipFactory
        ship = ShipFactory.create(Ship.DESTROYER, 'test_fleet')

        exception_raised = True
        try:
            ship.set_position(((0, 0),))
            exception_raised = False
        except Exception as ex:
            self.assertMatch("Ship wasn't positioned properly.", ex[0])

        self.assertEquals(True, exception_raised, 'Expected exception not raised')

    def test_ship_is_sunk(self):
        from BattleShips.factory import ShipFactory
        ship = ShipFactory.create(Ship.DESTROYER, 'test_fleet')
        ship.set_position(((0, 0), (0, 1), (0, 2), (0, 3)))
        ship_position = ship.get_position()

        for i in range(0, len(ship_position)-1):
            ship.add_damaged_part(ship_position[i])
            self.assertEquals(False, ship.is_sunk())

        ship.add_damaged_part(ship_position[len(ship_position) - 1])
        self.assertEquals(True, ship.is_sunk())




if __name__ == '__main__':
    unittest.main()
