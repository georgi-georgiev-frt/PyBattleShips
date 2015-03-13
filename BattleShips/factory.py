from entity import Ship


class ShipFactory(object):

    @staticmethod
    def create(ship_type, fleet_name):
        """
        Creating ships
        :param ship_type: tuple
        :param fleet_name: string
        :return: Ship
        """

        if isinstance(ship_type, (tuple, list)):
            return Ship(ship_type[1], ship_type[0], fleet_name)
        else:
            raise AttributeError('Provided ship type must be tuple / list')