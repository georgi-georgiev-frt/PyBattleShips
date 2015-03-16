import sys
from entity import BattleField, Fleet, Ship


class GameController(object):
    CHEAT_SHOW = 'show'
    MODE_TRANSPARENT_MAP = 1
    MODE_MASKED_MAP = 2

    def __init__(self):
        self._battle_field = None
        self._shot_codes = ()
        self.user_input = ''

        self._battle_field = BattleField(10, 10)
        fleet = Fleet('game_fleet', (
            (Ship.destroyer, 2),
            (Ship.fighter, 1),
        ), )

        self._battle_field.position_fleet(fleet)

        self._generate_shot_codes()

    def game_play(self, in_test_mode = False):
        draw = True
        try:
            draw = self._process_user_input()
        except Exception:
            print "*** Error ***"

        if draw:
            self._draw_field()

        if self._battle_field.success_shots < self._battle_field.get_ship_parts_count():
            if not in_test_mode:
                self._request_user_input()
                self.game_play()
        else:
            self._game_done()

    def _game_done(self):
        print 'Well done! You completed the game in {} shots'.format(
            str(self._battle_field.get_shots_count())
        )

    def _request_user_input(self):
        self.user_input = raw_input("Enter coordinates (row, col), e.g. A5 = ")

    def _process_user_input(self):
        user_input = self.user_input.strip().lower()
        if user_input is not '':
            if user_input not in self._shot_codes:
                raise Exception('Not allowed user input')

            if user_input == self.CHEAT_SHOW:
                self._draw_field(self.MODE_TRANSPARENT_MAP)
                return False

            user_shot = self._shot_codes[user_input]

            if user_shot in self._battle_field.get_shots():
                return True  # Already shot there - skipping

            ship = self._battle_field.add_shot(user_shot)
            if isinstance(ship, Ship):
                if ship.is_sunk():
                    print 'Sunk!'
                else:
                    print 'Right on target!'
            else:
                print 'Missed!'

        return True

    def _draw_field(self, mode=MODE_MASKED_MAP):
        sys.stdout.write('0')
        for i in range(0, self._battle_field.get_cols()):
            sys.stdout.write(str(i + 1)),  # cols indexes

        sys.stdout.write('\n')

        field = self._battle_field.get_field()
        shots = self._battle_field.get_shots()
        letters_map = self._battle_field.get_letters_map()

        for i in range(0, self._battle_field.get_rows()):
            sys.stdout.write(letters_map[i])  # rows indexes

            for j in range(0, self._battle_field.get_cols()):
                if (i, j) in field and ((i, j) in shots or mode == self.MODE_TRANSPARENT_MAP):
                    sys.stdout.write(BattleField.SHIP_PART)
                elif (i, j) in shots:
                    sys.stdout.write(BattleField.MISSED_SHOT)
                else:
                    if mode == self.MODE_MASKED_MAP:
                        sys.stdout.write(BattleField.WATER)
                    else:
                        sys.stdout.write(' ')

            sys.stdout.write('\n')

    def _generate_shot_codes(self):
        letters_map = self._battle_field.get_letters_map()
        shot_codes = {}
        for i in range(0, self._battle_field.get_rows()):
            for j in range(0, self._battle_field.get_cols()):
                shot_codes[letters_map[i].lower() + str(j+1)] = (i, j)

        shot_codes[self.CHEAT_SHOW] = 'cheat'
        self._shot_codes = shot_codes
