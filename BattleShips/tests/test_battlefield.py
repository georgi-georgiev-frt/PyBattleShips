import unittest

from BattleShips.tests.battleships_test import BattleShipsTest
from BattleShips.entity import BattleField
from BattleShips.entity import Fleet
from BattleShips.entity import Ship


class TestBattleField(BattleShipsTest):
    def setUp(self):
        pass

    def test_position_fleet(self):
        for i in range(0, 100):  # running the test 100 times
            self.position_fleet_test()

    def position_fleet_test(self):
        description = (
            (Ship.destroyer, 2),
            (Ship.fighter, 1)
        )
        fleet = Fleet('testing_fleet', description)

        battle_field = BattleField(10, 10)
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


if __name__ == '__main__':
    unittest.main()

