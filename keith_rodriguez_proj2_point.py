from keith_rodriguez_proj2_metapoint import MetaPoint


class Point(MetaPoint):

    def __init__(self, x0, y0, v0):
        self._x = x0
        self._y = y0
        self._v = v0

    def __repr__(self):
        return self._v

    def get_point(self):
        return [self._x, self._y, self._v]

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_value(self):
        return self._v
