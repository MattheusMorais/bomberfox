from model.Bomb import Bomb
from model.Helper import ENEMY_SYMBOL, OBSTACLE_DESTR, OBSTACLE_INDESTR, BOMB_SYMBOL, FLOOR_SYMBOL

class Player:
    """
    Representa o jogador no jogo, incluindo movimentação, colocação de bombas e controle de vida/morte.

    Attributes:
        SYMBOL (str): Símbolo que representa o jogador no mapa.
        spawn_position (tuple[int, int]): Posição inicial do jogador no mapa.
        directions (dict[str, tuple[int, int]]): Dicionário para mudança de posição.
        active_bombs (list[Bomb]): Lista de bombas ativas colocadas pelo jogador.
        current_position (tuple[int, int]): Posição atual do jogador.
        game_state (GameState): variavel para acessar o estado do jogo.
        player_alive (bool): Indica se o jogador está vivo, usado no método is_alive para definir lógica de morte do jogador na classe Gameplay.
    """   

    SYMBOL = "P"
    spawn_position = (1,1)
    directions = {
        "w" : (-1,0),
        "a" : (0,-1),
        "s" : (1,0),
        "d" : (0,1)
    }

    def __init__(self, game_state):
        self.active_bombs = []
        self.current_position = self.spawn_position
        self.game_state = game_state
        self.player_alive = True
        self.moved = False

    def move(self, move_command, game_map):
        if self.is_blocked(move_command, game_map):
            return False
            
        if move_command in self.directions:
            self.moved = True

            old_row, old_col = self.current_position
            drow, dcol = self.directions[move_command]

            new_row = old_row + drow
            new_col = old_col + dcol

            old_cell = game_map.matrix[old_row][old_col]
            new_cell = game_map.matrix[new_row][new_col]

            if old_cell == Bomb.SYMBOL:
                game_map.update_cell(old_row, old_col, Bomb.SYMBOL)
            else:
                game_map.update_cell(old_row, old_col, FLOOR_SYMBOL)

            if new_cell == Bomb.SYMBOL:
                game_map.update_cell(new_row, new_col, Bomb.SYMBOL)
            else:
                game_map.update_cell(new_row, new_col, Player.SYMBOL)

            self.current_position = (new_row, new_col)

            survived_turns = self.game_state.get_survived_turns()

            self.game_state.set_survived_turns(survived_turns+1)
                        
    def put_bomb(self, move_command, gamemap):
        if move_command == 'f':
            row, col = self.current_position

            gamemap.update_cell(row, col, Bomb.SYMBOL)

            bomb = Bomb(row, col, self.game_state)
            self.active_bombs.append(bomb)

            bombs_utilized = self.game_state.get_bombs_utilized()
            self.game_state.set_bombs_utilized(bombs_utilized + 1)
        
    def is_blocked(self, move_command, game_map):
        row, col = self.current_position

        if move_command in self.directions:
            drow, dcol = self.directions[move_command]

            new_row = row + drow
            new_col = col + dcol

            new_cell = game_map.matrix[new_row][new_col]

            return new_cell == OBSTACLE_DESTR or new_cell == OBSTACLE_INDESTR or new_cell == ENEMY_SYMBOL or new_cell == BOMB_SYMBOL
                
        return False
    
    def is_alive(self):
        return self.player_alive
    