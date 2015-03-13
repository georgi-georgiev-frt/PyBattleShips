import unittest

from BattleShips.tests.battleships_test import BattleShipsTest
from BattleShips.entity import BattleField
from BattleShips.entity import Fleet
from BattleShips.entity import Ship


class TestFleet(BattleShipsTest):
    def setUp(self):
        pass

    def test_fleet_creation(self):
        description = (
            (Ship.destroyer, 2),
            (Ship.fighter, 1)
        )
        fleet = Fleet('testing_fleet', description)

        fleet_ships = fleet.get_ships()

        self.assertEquals(2, len(fleet_ships['Destroyer']))
        self.assertEquals(1, len(fleet_ships['Fighter']))


if __name__ == '__main__':
    unittest.main()

