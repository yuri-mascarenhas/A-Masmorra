from PPlay.gameimage import *
from PPlay.sprite import *

class Tile(Sprite):
    """
    Define o Tile a ser criado
    """
    #--------------------Atributos--------------------
    layer: int
    id: int

    #--------------------Métodos--------------------
    def __init__(self, addr: str, frame: int, layer: int):
        super().__init__(addr, frame)
        
        self.set_total_duration(1000)
        self.layer = layer
    
    """Desenha o Tile nas posições x, y"""
    def draw_at(self, x: int, y: int):
        self.x = x
        self.y = y
        self.draw()

class Tileset(object):
    """
    Define o Tileset a ser criado
    """
    #--------------------Atributos--------------------
    layers: int
    tileset: list[Tile]

    #--------------------Métodos--------------------
    def __init__(self, tiles: list[Tile]):
        self.tileset = tiles
        self.layers = self[len(tiles) - 1].layer + 1

        for i in range(len(self)):
            self[i].id = i + 1

    """Retorna a quantidade de Tiles no Tileset"""
    def __len__(self):
        return len(self.tileset)

    """Retorna um Tile numa posião especifica"""
    def __getitem__(self, key):
        try:
            return self.tileset[key]
        except TypeError as e:
            print(e)
        except IndexError as e:
            print(e)

    """Seta um Tile numa posição especifica"""
    def __setitem__(self, key, value):
        try:
            self.tileset[key] = value
        except TypeError as e:
            print(e)
        except IndexError as e:
            print(e)

    """Acrescenta um valor ao Tileset"""
    def append(self, value):
        self.tileset.append(value)
