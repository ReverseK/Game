from keith_rodriguez_proj2_grid import Grid
from keith_rodriguez_proj2_abstractgame import Game
from keith_rodriguez_proj2_point import Point
from random import randint

class Battleship(Game, Grid):
    player1 = 'User'
    player2 = 'Computer'
    hit = 'X'
    miss = 'O'
    ships = [
        'Carrier',
        'Battleship',
        'Cruiser',
        'Submarine',
        'Destroyer'
    ]
    ship_sizes = {
        'Carrier': 5,
        'Battleship': 4,
        'Cruiser': 3,
        'Submarine': 3,
        'Destroyer': 2
    }
    turn_num = 1
    grid_width = 10
    grid_height = 10

    def __init__(self, player1, player2):
        self._user = player1
        self._comp = player2
        self._game_over = False
        self._grid = Grid(10, 10)
        self._user_grid = Grid(10, 10)
        self._comp_hidden_grid = Grid(10, 10)
        self._comp_seen_grid = Grid(10, 10)
        self._ships = Battleship.ships
        self._carrier = 'Carrier'
        self._battleship = 'Battleship'
        self._cruiser = 'Cruiser'
        self._submarine = 'Submarine'
        self._destroyer = 'Destroyer'
        self._user_ships_set = []
        self._user_ship_locations = {}
        self._user_set_cells = []
        self._user_used_cells = set()
        self._user_ships_sank = []
        self._comp_ships_set = []
        self._comp_ship_locations = {}
        self._comp_set_cells = []
        self._comp_used_cells = set()
        self._comp_ships_sank = []

    def game_play(self):
        self.game_start()
        while self._game_over is not True:
            if self.turn_num % 2 == 1:
                print(self._comp_seen_grid)
                print('\nThese Computer ships sank:')
                print(self._comp_ships_sank)
                print(self._comp_ship_locations)
                self.player_turn('User')
                self.did_ship_sink()
                self.is_game_over()
            elif self.turn_num % 2 == 0:
                self.player_turn('Computer')
                print(self._user_grid)
                self.did_ship_sink()
                self.is_game_over()
                print('\nThese User ships sank:')
                print(self._user_ships_sank)
        play_again = input('Would you like to play again? (Y/N)').upper()
        try:
            if play_again == 'Y':
                self.__init__(self.player1, self.player2)
                self.game_start()
            elif play_again == 'N':
                print('Okay, some other time')
        except Exception:
            pass

    def game_start(self):
        print('Let\'s play some Battleship.')
        print('You\'ll need to set your five ships of varying length:')
        print('Carrier, 5 units.')
        print('Battleship, 4 units.')
        print('Cruiser and Submarine, 3 units.')
        print('Destroyer, 2 units.')
        print('All ships\'s noses point either left or up on a 10x10 grid,')
        print('so they should not be placed too far down or to the right.')
        print('All incompatibilities for placement will force you to try again,')
        print('The computer\'s ships will be randomly assigned.\n')
        user_input = input('Shall we begin? (Y/N)\n').upper()
        if user_input == 'Y':
            self.comp_set_ships()
            self.user_set_ships()
        elif user_input == 'N':
            print('\nAnother time.')
            pass
        else:
            self.game_start()

    def comp_set_ships(self):
        while 'Carrier' not in self._comp_ships_set:
            self.comp_set_ship('Carrier')
        while 'Battleship' not in self._comp_ships_set:
            self.comp_set_ship('Battleship')
        while 'Cruiser' not in self._comp_ships_set:
            self.comp_set_ship('Cruiser')
        while 'Submarine' not in self._comp_ships_set:
            self.comp_set_ship('Submarine')
        while 'Destroyer' not in self._comp_ships_set:
            self.comp_set_ship('Destroyer')
        self._comp_used_cells = set()

    def user_set_ships(self):
        while 'Carrier' not in self._user_ships_set:
            self.user_set_ship('Carrier')
        while 'Battleship' not in self._user_ships_set:
            self.user_set_ship('Battleship')
        while 'Cruiser' not in self._user_ships_set:
            self.user_set_ship('Cruiser')
        while 'Submarine' not in self._user_ships_set:
            self.user_set_ship('Submarine')
        while 'Destroyer' not in self._user_ships_set:
            self.user_set_ship('Destroyer')
        self._user_used_cells = set()

    def comp_set_ship(self, ship):
        ship_length = self.ship_sizes.get(ship)
        comp_h_or_v = randint(0, 1)
        comp_x = randint(0, (10 - ship_length))
        comp_y = randint(0, (10 - ship_length))
        if comp_h_or_v == 0:
            for i in range(ship_length):
                if (comp_x + i, comp_y) in self._comp_used_cells:
                    return
            for i in range(ship_length):
                self._comp_hidden_grid.set_point(Point(comp_x + i, comp_y, 'O'), 'O')
                self._comp_used_cells.add((comp_x + i, comp_y))
                self._comp_set_cells.append((comp_x + i, comp_y))
            self._comp_ship_locations[ship] = set(self._comp_set_cells)
            self._comp_ships_set.append(ship)
        elif comp_h_or_v == 1:
            for i in range(ship_length):
                    if (comp_x, comp_y + i) in self._comp_used_cells:
                        return
            for i in range(ship_length):
                self._comp_hidden_grid.set_point(Point(comp_x, comp_y + i, 'O'), 'O')
                self._comp_used_cells.add((comp_x, comp_y + i))
                self._comp_set_cells.append((comp_x, comp_y + i))
            self._comp_ship_locations[ship] = set(self._comp_set_cells)
            self._comp_ships_set.append(ship)
        self._comp_set_cells = []

    def user_set_ship(self, ship):
        length_ship = self.ship_sizes.get(ship)
        print('\nNow to set your: ' + ship + '\nIt is ' + str(length_ship) + ' units long')
        user_input = input('Do you wish to place it horizontally or vertically? (H/V)\n').upper()
        try:
            if user_input == 'H':
                print('\nHorizontal it is then.\n')
                x_input = int(input('Where do you want your x-coordinate?\n'))
                y_input = int(input('Where do you want your y-coordinate?\n'))
                for i in range(length_ship):
                    if (x_input + i, y_input) in self._user_used_cells:
                        print('\n*** You have used some of those cells already - try again ***')
                        return
                    if x_input + i >= self.grid_width:
                        print('\n*** You cannot place that so far to the right - try again. ***')
                        return
                for i in range(length_ship):
                    self._user_grid.set_point(Point(x_input + i, y_input, 'O'), 'O')
                    self._user_used_cells.add((x_input + i, y_input))
                    self._user_set_cells.append((x_input + i, y_input))
                self._user_ship_locations[ship] = set(self._user_set_cells)
                self._user_ships_set.append(ship)
                print(self._user_grid)
            elif user_input == 'V':
                print('\nVertical it is then.\n')
                x_input = int(input('Where do you want your x-coordinate?\n'))
                y_input = int(input('Where do you want your y-coordinate?\n'))
                for i in range(length_ship):
                    if (x_input, y_input + i) in self._user_used_cells:
                        print('\n*** You have used some of those cells already - try again ***')
                        return
                    if y_input + i >= self.grid_height:
                        print('\n*** You cannot place that so far down - try again. ***')
                        return
                for i in range(length_ship):
                    self._user_grid.set_point(Point(x_input, y_input + i, 'O'), 'O')
                    self._user_used_cells.add((x_input, y_input + i))
                    self._user_set_cells.append((x_input, y_input + i))
                self._user_ship_locations[ship] = set(self._user_set_cells)
                self._user_ships_set.append(ship)
                print(self._user_grid)
            else:
                print('\n*** Please enter an H or V ***')
            self._user_set_cells = []
        except Exception:
            return

    def hit_or_miss(self, point, player):
        x = point.get_x()
        y = point.get_y()
        if player == 'User':
            value = self._comp_hidden_grid._grid[y][x].get_value()
            try:
                if value == '*':
                    self._comp_seen_grid.set_point(point, '@')
                    print('MISS!')
                elif value == 'O':
                    self._comp_seen_grid.set_point(point, 'X')
                    print('HIT!')
            except Exception:
                print('\n*** That space won\'t work - try again. ***')
        elif player == 'Computer':
            value = self._user_grid._grid[y][x].get_value()
            try:
                if value == '*':
                    self._user_grid.set_point(point, '@')
                    print('MISS!')
                if value == 'O':
                    self._user_grid.set_point(point, 'X')
                    print('HIT!')
            except Exception:
                print('*** That space won\'t work - try again. ***')

    def did_ship_sink(self):
        for ship in self.ships:
            user_ship = self._user_ship_locations[ship]
            comp_ship = self._comp_ship_locations[ship]
            if len(user_ship & self._comp_used_cells) == len(user_ship):
                if ship not in self._user_ships_sank:
                    print('\nUser\'s ' + ship + ' sank!')
                    self._user_ships_sank.append(ship)
            if len(comp_ship & self._user_used_cells) == len(comp_ship):
                if ship not in self._comp_ships_sank:
                    print('\nComputer\'s ' + ship + ' sank!')
                    self._comp_ships_sank.append(ship)

    def is_game_over(self):
        if len(self._user_ships_sank) == 5:
            print('Game over! The Computer wins!')
            self._game_over = True
        elif len(self._comp_ships_sank) == 5:
            print('Game over! The User wins!')
            self._game_over = True
        else:
            self._game_over = False

    def player_turn(self, player):
        print('\nIt is now the ' + player + '\'s turn.')
        try:
            if player == 'User':
                user_x = int(input('Please enter your desired x coordinate. (0-9)\n'))
                user_y = int(input('Please enter your desired y coordinate. (0-9)\n'))
                try:
                    if (user_x, user_y) not in self._user_used_cells:
                        self.hit_or_miss(Point(user_x, user_y, ''), 'User')
                        self._user_used_cells.add((user_x, user_y))
                        self.turn_num += 1
                    elif (user_x, user_y) in self._user_used_cells:
                        print('\n*** You have used that point - try again. ***')
                except Exception:
                    print('\n*** That won\'t work - try again. ***')
            elif player == 'Computer':
                comp_x = randint(0, 9)
                comp_y = randint(0, 9)
                try:
                    if (comp_x, comp_y) not in self._comp_used_cells:
                        self.hit_or_miss(Point(comp_x, comp_y, ''), 'Computer')
                        self._comp_used_cells.add((comp_x, comp_y))
                        self.turn_num += 1
                    elif (comp_x, comp_y) in self._comp_used_cells:
                        print('\n*** You have used that point - try again. ***')
                except Exception:
                    print('\nThe computer messed up - it\'s trying again.')
        except Exception:
            pass


def main():
    battle = Battleship(Battleship.player1, Battleship.player2)
    # battle.comp_set_ships()
    # print(battle._comp_hidden_grid)
    # print(battle._comp_used_cells)
    # print(len(list(unique_everseen(battle._comp_used_cells))))
    # print(battle._comp_ship_locations)
    # print(len(battle._comp_used_cells))
    battle.game_play()


if __name__ == '__main__':
    main()
