import string


class GameBoard(object):
    """
    Basic game board that can be used in any game with x-y board
    """
    def __init__(self, rows, cols):
        """
        :param rows: int
        :param cols: int
        :return:
        """
        self._rows = 0
        self._cols = 0
        self._rows_letters = ()
        self._letters_map = {}

        if rows > 26:
            raise Exception('Max 26 rows exceeded')  # Limiting game board rows from A to Z

        self._rows = rows
        self._cols = cols

        letters = list(string.ascii_uppercase)
        rows_letters = []
        for i in range(0, rows):
            letter = letters[i]
            rows_letters.append(letter)
            self._letters_map[i] = letter

        self._rows_letters = tuple(rows_letters)

    def get_rows(self):
        """
        :return: int
        """
        return self._rows

    def get_cols(self):
        """
        :return: int
        """
        return self._cols

    def get_rows_letters(self):
        """
        :return: (string)
        """
        return self._rows_letters

    def get_letters_map(self):
        """
        :return: dict[int, string]
        """
        return self._letters_map


class BattleField(GameBoard):
    """
    BattleShips battlefield
    """
    WATER = '.'
    SHIP_PART = 'X'
    MISSED_SHOT = '-'
    HORIZONTAL = '0'
    VERTICAL = '1'
    RESULT_MISS = False

    def __init__(self,  rows, cols):
        """
        :param rows: int
        :param cols: int
        :return:
        """
        self._field = {}
        self._fleets = []
        self._shots = []
        self.success_shots = 0

        super(self.__class__, self).__init__(rows, cols)

    def position_fleet(self, fleet):
        """
        Positioning fleet of ships on the battle field
        :param fleet: Fleet
        """
        fleet_ships = fleet.get_ships()

        for group_name in fleet_ships:
            ships_list = fleet_ships[group_name]
            for ship in ships_list:
                self._position_ship(ship)

        self._fleets.append(fleet)

    def _position_ship(self, ship):
        """
        Positioning single ship on the battle field
        :param ship: Ship
        :return:
        """
        import random

        ship_length = ship.get_length()
        available_positions = self._scan_field(ship_length)
        ship_position = []

        if len(available_positions[self.HORIZONTAL]) > 0 and len(available_positions[self.VERTICAL]) > 0:
            orientation = str(random.randint(0, 1))
        elif len(available_positions[self.HORIZONTAL]) > 0:
            orientation = self.HORIZONTAL
        elif len(available_positions[self.VERTICAL]) > 0:
            orientation = self.VERTICAL
        else:
            raise Exception("Can't place fleet ships. Too much ships on a small field.")

        selected_available_positions = available_positions[orientation]
        start_position_rand = random.randint(0, len(selected_available_positions)-1)
        start = available_positions[orientation][start_position_rand]

        for i in range(0, ship_length):
            if orientation == self.HORIZONTAL:
                coordinates = (start[0], start[1]+i)
            else:
                coordinates = (start[0]+i, start[1])
            self._field[coordinates] = ship
            ship_position.append(coordinates)

        ship.set_position(tuple(ship_position))

    def _scan_field(self, ship_length):
        """
        Finding all available start points for positioning a given ship_length
        :param ship_length: int
        :return:
        """
        available_positions = {
            self.HORIZONTAL: [],
            self.VERTICAL: []
        }

        i = 0
        while i < self._rows:
            j = 0
            while j < self._cols:
                if j + ship_length > self._cols:  # If there isn't enough room to place that ship horizontally
                    break

                for k in range(0, ship_length):
                    if (i, j+k) in self._field:  # If there is already allocated sector in that row
                        j += k  # move cursor to the col after allocated sector
                        break
                else:
                    available_positions[self.HORIZONTAL].append((i, j))
                j += 1
            i += 1

        j = 0
        while j < self._rows:
            i = 0
            while i < self._cols:
                if i + ship_length > self._cols:  # If there isn't enough room to place that ship vertically
                    break

                for k in range(0, ship_length):
                    if (i + k, j) in self._field:  # If there is already allocated sector in that col
                        i += k  # move cursor to the row after allocated sector
                        break
                else:
                    available_positions[self.VERTICAL].append((i, j))
                i += 1
            j += 1
        return available_positions

    def get_positioned_fleets(self):
        """
        Returning all positioned fleets on the battle field
        :return: list[Fleet]
        """
        return self._fleets

    def get_field(self):
        """
        Get field dict containing all ships
        :return: dict[(int,int),Ship]
        """
        return self._field

    def get_shots(self):
        """
        Returns list of all made shots during the game
        :return: list[(int,int)]
        """
        return self._shots

    def add_shot(self, shot):
        """
        Appending shot and returning hit ship or False
        :param shot: (int, int)
        :return: Ship | False
        """
        self._shots.append(shot)

        if shot in self._field:
            self.success_shots += 1
            ship = self._field[shot]
            ship.add_damaged_part(shot)
            return ship
        else:
            return self.RESULT_MISS

    def get_shots_count(self):
        """
        How many shots are already made
        :return: int
        """
        return len(self._shots)

    def get_ship_parts_count(self):
        """
        How many ship parts are on the battle field
        :return: int
        """
        return len(self._field)


class Ship(object):
    """
    The ship
    """
    destroyer = ('Destroyer', 4)
    fighter = ('Fighter', 5)

    def __init__(self, length, name, fleet_name):
        """
        :param length: int
        :param name: string
        :param fleet_name: string
        """
        self._length = 0
        self._name = ''
        self._fleet_name = ''
        self._position = ()
        self._damaged_parts = []

        self._length = length
        self._name = name
        self._fleet_name = fleet_name

    def get_length(self):
        """
        :return: int
        """
        return self._length

    def get_name(self):
        """
        :return: string
        """
        return self._name

    def is_positioned(self):
        """
        :return: True|False
        """
        return len(self._position) == self._length

    def get_position(self):
        """
        :return: ((int,int))
        """
        return self._position

    def set_position(self, position):
        """
        :param position: ((int,int))
        """
        self._position = position

        if not self.is_positioned():
            self._position = ()
            raise Exception("Ship wasn't positioned properly.")

    def add_damaged_part(self, part):
        """
        Adding ship damaged part to damaged parts list
        :param part: (int, int)
        """
        self._damaged_parts.append(part)

    def is_sunk(self):
        """
        Is ship sunk
        :return: True|False
        """
        return len(self._damaged_parts) == self._length

    def __str__(self):
        """
        The string representation of the ship (used for debugging)
        :return: string
        """
        position = ''
        if self.is_positioned():
            position = ", position({},{})".format(self._position[0], self._position[-1])
        return "(id: {}, name: {}, fleet: {}{})".format(id(self), self.get_name(), self._fleet_name, position)


class Fleet(object):
    def __init__(self, name, description):
        """
        :param name: string
        :param description: (((string, int), int), int)
        """
        self.name = ''
        self.description = ()
        self._ships = {}

        self.name = name
        if isinstance(description, tuple):
            self.description = description
        else:
            raise AttributeError('Fleet description must be tuple')

        self.create_ships()

    def create_ships(self):
        """
        Creating ships for a fleet
        """
        from factory import ShipFactory

        self._ships = {}

        for ship_description, count in self.description:
            for i in range(0, count):
                ship = ShipFactory.create(ship_description, self.name)
                ship_name = ship.get_name()
                try:
                    self._ships[ship_name].append(ship)
                except KeyError:
                    self._ships[ship_name] = []
                    self._ships[ship_name].append(ship)

    def get_ships(self):
        """
        :return: dict[string, list[Ship]]
        """
        return self._ships
