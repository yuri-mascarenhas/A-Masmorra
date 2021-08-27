from PPlay.gameimage import *
from math import ceil
from tile import *
from copy import copy

class Map(object):
    """
    Define o Mapa a ser construído/salvo
    """
    #--------------------Atributos--------------------
    _map: list[list[list[Tile]]] = []            # Matriz de Tiles com as posições já setadas
    _map_loader: list[list[list[Tile]]] = []     # Matriz com os códigos carregados do arquivo
    _canvas: Tileset

    lines: int
    columns: int
    layers: int
    _grid = { "x": 0, "y": 0 }

    _background: GameImage
    _default_tile: str

    #--------------------Métodos--------------------
    def __init__(self, size_x: int, size_y: int, grid_x: int, grid_y: int, tile_set: Tileset, layers: int = 1, default_background: str = "resources/background/default.png", default_tile: str ="resources/null.png ", file_name: str = "resources/maps/map1.txt"):
        self.columns = ceil(size_x / grid_x)
        self.lines = ceil(size_y / grid_y)
        self.layers = layers

        self._grid["x"] = grid_x
        self._grid["y"] = grid_y

        self._background = GameImage(default_background)
        self._default_tile = default_tile
        self._canvas = tile_set

        self.load_map(file_name)        
 
    """Importa o mapa do arquivo especificado"""
    def load_map(self, file_name: str):
        file = open(file_name, 'r')
        for z in range(self.layers):
            self._map_loader.append([])
            for y in range(self.columns + 1):
                curr_line = file.readline().split()
                if(len(curr_line) > 1):
                    self._map_loader[z].append([])
                    for x in range(self.lines):
                        if(int(curr_line[x]) > 0):
                            curr_tile = copy(self._canvas[int(curr_line[x]) - 1])
                            self._map_loader[z][y].append(curr_tile)
                        else:
                            self._map_loader[z][y].append(None)
        file.close()
        # Transposição
        for z in range(self.layers):
            self._map.append([])
            for x in range(self.lines):
                self._map[z].append([])
                for y in range(self.columns):
                    self._map[z][x].append(copy(self._map_loader[z][y][x]))
                    if(self._map_loader[z][y][x] != None):
                        self._map[z][x][y].x = y * self._grid["y"]
                        self._map[z][x][y].y = x * self._grid["y"]

    """Desenha a camada específica da matriz-mapa"""
    def draw_layer(self, layer: int):
        if(layer <= self.layers):
            for x in range(self.lines):
                for y in range(self.columns):
                    if(self._map[layer][x][y] != None):
                        self._map[layer][x][y].draw()

    """Retorna o Tile de uma posição expecífica da matriz-mapa"""
    def get_tile(self, layer: int, line: int, column: int):
        return self._map[layer][line][column]

    """Retorna a camada específica da matriz-mapa"""
    def get_layer(self, layer: int):
        return self._map[layer]

    def get_grid_size(self):
        return self._grid["x"]

    """Muda o Tile de uma posição expecífica da matriz-mapa"""
    def set_tile(self, tile: Tile, layer: int, line: int, column: int):
        self._map[layer][line][column] = copy(tile)
    
    """Apaga o Tile de uma posição expecífica da matriz-mapa"""
    def delete_tile(self, layer: int, line: int, column: int):
        self._map[layer][line][column] = Tile(self._default_tile, 1, layer)
    
    """Limpa todos os elementro da matriz-mapa"""
    def clear(self):
        for z in range(self.layers):
            for x in range(self.lines):
                for y in range(self.columns):
                    self.delete_tile(z, x, y)

