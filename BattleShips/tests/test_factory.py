from BattleShips.tests import BattleShipsTest
from BattleShips.factory import ShipFactory


class TestFactory(BattleShipsTest):

    def setUp(self):
        pass

    # ShipFactory tests

    def test_create_ships(self):
        from BattleShips.entity import Ship

        destroyer_from_factory = ShipFactory.create(Ship.destroyer,  'test_fleet')
        destroyer = Ship(Ship.destroyer[1], Ship.destroyer[0], 'test_fleet')
        self.compare_ships(destroyer_from_factory, destroyer)

        fighter_from_factory = ShipFactory.create(Ship.fighter, 'test_fleet')
        fighter = Ship(Ship.fighter[1], Ship.fighter[0], 'test_fleet')
        self.compare_ships(fighter_from_factory, fighter)

    def test_invalid_ship_type_raises_exception(self):
        exception_raised = True
        try:
            ShipFactory.create('invalid data', 'test_fleet')
            exception_raised = False
        except Exception as ex:
            self.assertMatch('Provided ship type must be tuple', ex[0])

        self.assertEquals(True, exception_raised, 'Expected exception not raised')

    def compare_ships(self, factory_ship, on_the_fly_ship):
        self.assertEquals(factory_ship.__class__.__name__, on_the_fly_ship.__class__.__name__)
        self.assertEquals(factory_ship.get_length(), on_the_fly_ship.get_length())
        self.assertEquals(factory_ship.get_name(), on_the_fly_ship.get_name())

if __name__ == '__main__':
    unittest.main()

