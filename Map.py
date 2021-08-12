from PPlay.gameimage import *
from PPlay.sprite import *
import copy

class Map(object):
    #--------------------Atributos--------------------
    _map = []
    _canvas = []
    _lines = 0
    _columns = 0

    #--------------------Métodos--------------------
    def __init__(self, name, lines, columns):
        self._canvas = [Sprite("assets/tiles/chao0.png"),
                        Sprite("assets/tiles/paredeCID.png"),
                        Sprite("assets/tiles/paredeCIE.png"),
                        Sprite("assets/tiles/paredeCSD.png"),
                        Sprite("assets/tiles/paredeCSE.png"),
                        Sprite("assets/tiles/paredeMI.png"),
                        Sprite("assets/tiles/paredeMS.png"),
                        Sprite("assets/tiles/paredeTriID.png"),
                        Sprite("assets/tiles/paredeTriIE.png"),
                        Sprite("assets/tiles/paredeTriSD.png"),
                        Sprite("assets/tiles/paredeTriSE.png"),
                        Sprite("assets/tiles/paredeE.png"),
                        Sprite("assets/tiles/paredeD.png"),
                        Sprite("assets/tiles/null.png")]
        self._lines = lines
        self._columns = columns
        self.load_map(name)

    """Importa o mapa do arquivo para este objeto"""
    def load_map(self, name):
        file = open(name, 'r')
        for i in range(self._lines):
            self._map.append([])
            for j in range(self._columns):
                tile_code = int(file.readline())
                tile = copy.copy(self._canvas[tile_code])
                self._map[i].append(tile)
        self.position_tiles()

    """Posiciona as Sprites de cada elemento da matriz-mapa"""
    def position_tiles(self):
        for i in range(self._lines):
            for j in range(self._columns):
                self._map[i][j].x = j * 48
                self._map[i][j].y = i * 48

    def draw(self):
        for i in range(self._lines):
            for j in range(self._columns):
                self._map[i][j].draw()