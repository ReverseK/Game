from keith_rodriguez_proj2_metagrid import MetaGrid
from keith_rodriguez_proj2_point import Point


class Grid(MetaGrid):

    def __init__(self, w, h):
        self._w = w
        self._h = h
        self._grid = self.mk_grid()

    def __repr__(self):
        row_strings = []
        print('')
        for row in self._grid:
            row_values = map(lambda i: i.get_value(), row)
            row_string = ' '.join(row_values)
            row_strings.append(row_string)
        return '\n'.join(row_strings) + '\n'

    def mk_grid(self):
        grid = []
        num_cols = self._w
        num_rows = self._h
        for row in range(num_rows):
            grid.append([])
            for col in range(num_cols):
                grid[-1].append(Point(col, row, '*'))
        return grid

    def print_coordinates(self):
        grid_coordinates = [(x, y) for x in range(self._w) for y in range(self._h)]
        print(grid_coordinates)

    def get_point(self, point):
        x = point.get_x()
        y = point.get_y()
        return self._grid[x][y]

    def get_values(self):
        cell_values = [self._grid[x][y].get_value() for x in range(self._w) for y in range(self._h)]
        return cell_values

    def set_point(self, point, point_value):
        x = point.get_x()
        y = point.get_y()
        self._grid[y][x] = Point(x, y, point_value)

    def ttt_check_point(self, point, point_value):
        x = point.get_x()
        y = point.get_y()
        value = self._grid[y][x].get_value()
        try:
            if value == '*':
                self.set_point(point, point_value)
        except:
            print('\n*** That space has been used - try again. ***')

    def bs_check_point(self, point):
        x = point.get_x()
        y = point.get_y()
        value = self._grid[y][x].get_value()
        try:
            if value == '*':
                self.set_point(point, 'O')
                print('MISS!')
            if value == '+':
                self.set_point(point, 'X')
                print('HIT!')
        except:
            print('\n*** That space won\'t work - try again. ***')

# def main():
#     game_grid = Grid(3, 3)
#     print(game_grid)
#     game_grid.check_point(Point(0, 0, 'O'))
#     print(game_grid.get_values())
#     game_grid.check_point(Point(0, 0, 'X'))
#     print(game_grid)
#
# if __name__ == '__main__':
#     main()
