from entity import Ship


class ShipFactory(object):
    """
    Ship factory for creating ships
    [StaticFactory DP] https://github.com/georgi-georgiev-frt/python-patterns/blob/master/static_factory.py
    """

    @staticmethod
    def create(ship_type, fleet_name):
        """
        Creating ships
        :param ship_type: (string, int)
        :param fleet_name: string
        :return: Ship
        """

        if isinstance(ship_type, (tuple, list)):
            return Ship(ship_type[1], ship_type[0], fleet_name)
        else:
            raise AttributeError('Provided ship type must be tuple / list')
