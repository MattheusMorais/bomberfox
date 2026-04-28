import random
from model.Helper import OBSTACLE_DESTR, OBSTACLE_INDESTR, BOMB_SYMBOL, PLAYER_SYMBOL, FLOOR_SYMBOL

class Enemy:
    """
    Representa um inimigo no mapa, capaz de se mover aleatoriamente 
    e colidir com obstáculos, bombas ou o jogador.

    Attributes:
        SYMBOL (str): Símbolo usado para representar o inimigo no mapa.
        directions (dict): Dicionário de movimentos possíveis (w,a,s,d).
        current_position (tuple): Tupla (linha, coluna) indicando a posição atual.
    """

    SYMBOL = "E"
    directions = {
        "w" : (-1,0),
        "a" : (0,-1),
        "s" : (1,0),
        "d" : (0,1)
        }

    def __init__(self, current_position):
        self.current_position = current_position

    def is_blocked(self, new_row, new_col, game_map):
        cell = game_map.matrix[new_row][new_col]
        if cell == OBSTACLE_DESTR or cell == OBSTACLE_INDESTR or cell == BOMB_SYMBOL or cell == Enemy.SYMBOL:
            return True
            
        return False

    def move(self, game_map):
        player_hit = False
        old_row, old_col = self.current_position

        row, col = random.choice(list(self.directions.values()))

        new_row = old_row + row
        new_col = old_col + col

        if self.is_blocked(new_row, new_col, game_map):
            return False

        if (game_map.matrix[new_row][new_col] == PLAYER_SYMBOL):
            player_hit = True

            self.current_position = (new_row, new_col)
            return player_hit
        
        game_map.matrix[old_row][old_col] = FLOOR_SYMBOL
        game_map.matrix[new_row][new_col] = Enemy.SYMBOL

        game_map.update_cell(old_row, old_col, FLOOR_SYMBOL)
        game_map.update_cell(new_row, new_col, Enemy.SYMBOL)
        self.current_position = (new_row, new_col)

        return False
        