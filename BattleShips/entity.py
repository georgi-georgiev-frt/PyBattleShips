import string


class GameBoard(object):
    def __init__(self, rows, cols):
        self._rows = 0
        self._cols = 0
        self._rows_letters = ()
        self._letters_map = {}

        if rows > 26:
            raise Exception('Max 26 rows exceeded')

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
        return self._rows

    def get_cols(self):
        return self._cols

    def get_rows_letters(self):
        return self._rows_letters

    def get_letters_map(self):
        return self._letters_map


class BattleField(GameBoard):
    water = '.'
    ship_part = 'X'
    missed_shot = '-'
    horizontal = '0'
    vertical = '1'
    result_miss = False

    def __init__(self,  rows, cols):
        self._field = {}
        self._fleets = []
        self._shots = []
        self.success_shots = 0

        super(self.__class__, self).__init__(rows, cols)

    def position_fleet(self, fleet):
        """
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

        :param ship:
        :return:
        """
        import random

        ship_length = ship.get_length()
        available_positions = self._scan_field(ship_length)
        ship_position = []

        if len(available_positions[self.horizontal]) > 0 and len(available_positions[self.horizontal]) > 0:
            orientation = str(random.randint(0, 1))
        elif len(available_positions[self.horizontal]) > 0:
            orientation = self.horizontal
        elif len(available_positions[self.vertical]) > 0:
            orientation = self.vertical
        else:
            raise Exception("Can't place fleet ships. Too much ships on a small field.")

        selected_available_positions = available_positions[orientation]
        start_position_rand = random.randint(0, len(selected_available_positions)-1)
        start = available_positions[orientation][start_position_rand]

        for i in range(0, ship_length):
            if orientation == self.horizontal:
                coordinates = (start[0], start[1]+i)
            else:
                coordinates = (start[0]+i, start[1])
            self._field[coordinates] = ship
            ship_position.append(coordinates)

        ship.set_position(tuple(ship_position))

    def _scan_field(self, ship_length):
        """
        Finding all available start points for positioning a given ship_length
        :param ship_length:
        :return:
        """
        available_positions = {
            self.horizontal: [],
            self.vertical: []
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
                    available_positions[self.horizontal].append((i, j))
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
                    available_positions[self.vertical].append((i, j))
                i += 1
            j += 1
        return available_positions

    def get_positioned_fleets(self):
        return self._fleets

    def get_field(self):
        return self._field

    def get_shots(self):
        return self._shots

    def add_shot(self, shot):
        self._shots.append(shot)

        if shot in self._field:
            self.success_shots += 1
            ship = self._field[shot]
            ship.add_damaged_part(shot)
            return ship
        else:
            return self.result_miss

    def get_shots_count(self):
        return len(self._shots)

    def get_ship_parts_count(self):
        return len(self._field)


class Ship(object):
    destroyer = ('Destroyer', 4)
    fighter = ('Fighter', 5)

    def __init__(self, length, name, fleet_name):
        """
        :param length: int
        :param name: string
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
        return self._length

    def get_name(self):
        return self._name

    def is_positioned(self):
        return len(self._position) == self._length

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

        if not self.is_positioned():
            self._position = ()
            raise Exception("Ship wasn't positioned properly.")

    def add_damaged_part(self, part):
        self._damaged_parts.append(part)

    def is_sunk(self):
        return len(self._damaged_parts) == self._length

    def __str__(self):
        position = ''
        if self.is_positioned():
            position = ", position({},{})".format(self._position[0], self._position[-1])
        return "(id: {}, name: {}, fleet: {}{})".format(id(self), self.get_name(), self._fleet_name, position)


class Fleet(object):
    def __init__(self, name, description):
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
        return self._ships
