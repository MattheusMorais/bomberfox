import random
from model.Helper import ENEMY_SYMBOL, FLOOR_SYMBOL, EXPLOSION_SYMBOL
from model.Obstacles import Obstacles
from model.Player import Player
from model.Bomb import Bomb

class Map:
    """
    Representa o mapa do jogo, contendo o jogador, inimigos, obstáculos e suas interações.

    Attributes:
        game_state: Objeto que mantém o estado do jogo.
        size (int): Dimensão do mapa (matriz quadrada).
        player_row (int): Linha da posição inicial do jogador.
        player_col (int): Coluna da posição inicial do jogador.
        initial_number_of_enemies (int): Quantidade iniscial de inimigos no jogo.
        enemy_quantity (int): Quantidade total de inimigos no mapa.
        obstacles (list): Lista de obstáculos no mapa (instância + posição).
        num_obstacles (int): Número de obstáculos a serem criados.
        min_distance_from_border (int): Distância mínima entre obstáculos/jogador e bordas.
        matrix (list): Representação 2D do mapa.
    """

    def __init__(self, game_state):
        self.game_state = game_state
        self.renderer = None
        self.matrix = None
        self.size = 12
        self.player_row, self.player_col = Player.spawn_position
        self.initial_number_of_enemies = game_state.get_enemy_start()
        self.enemy_quantity = game_state.get_enemy_quantity()
        self.obstacles = []
        self.num_obstacles = 3
        self.min_distance_from_border = 3
        self.create_map()

    def create_map(self):
        self.matrix = [[FLOOR_SYMBOL for _ in range(self.size)] for _ in range(self.size)]

        # Cria paredes indestrutiveis para delimitar o mapa
        for i in range(self.size):
            for j in range(self.size):
                if i==0 or i== self.size-1 or j == 0 or j == self.size-1:
                    self.matrix[i][j] = Obstacles.INDESTR
    
        # Cria obstaculos no mapa
        while len(self.obstacles) < self.num_obstacles:
            row = random.randint(1, self.size - 2)  
            col = random.randint(1, self.size - 2)

            if self.matrix[row][col] == FLOOR_SYMBOL:
                if abs(row - self.player_row) + abs(col - self.player_col) >= self.min_distance_from_border:

                    obstacle = Obstacles(self.game_state)

                    if obstacle.is_destructable():
                        self.matrix[row][col] = Obstacles.DESTR
                    else:
                        self.matrix[row][col] = Obstacles.INDESTR

                    self.obstacles.append((obstacle, row, col))

        # Coloca o jogador no mapa
        row, col = Player.spawn_position
        self.matrix[row][col] = Player.SYMBOL

        return self.matrix
    
    def get_free_positions(self):
        free_positions = []
        min_distance_from_player = 3

        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == FLOOR_SYMBOL:  
                    if abs(i - self.player_row) + abs(j - self.player_col) >= min_distance_from_player:
                        free_positions.append((i, j))
        return free_positions
    
    def is_index_valid(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size
            
    def update_cell(self, row, col, symbol):
        if self.is_index_valid(row, col):
            self.matrix[row][col] = symbol
            self.renderer.draw(row, col, symbol)
        else:
            print(f"Tentativa de atualizar célula inválida: ({row},{col})")
    
    def restore_cells(self, original_cells):
        for (row, col), original_cell in original_cells.items():
            if original_cell == Obstacles.DESTR:
                self.update_cell(row, col, FLOOR_SYMBOL)
            elif original_cell in [ENEMY_SYMBOL, Player.SYMBOL, Bomb.SYMBOL]:
                self.update_cell(row, col, FLOOR_SYMBOL)
            else:
                self.update_cell(row, col, original_cell)

    def chain_explosion(self, bomb, player_1, enemies):
        explosion_tiles = bomb.get_explosion_tiles()
        original_cells = {}

        for row, col in explosion_tiles:
            if not self.is_index_valid(row, col):
                continue

            cell = self.matrix[row][col]

            if cell == Obstacles.INDESTR:
                continue
                    
            original_cells[(row, col)] = cell
            self.update_cell(row, col, EXPLOSION_SYMBOL)

        hit_enemies = []
        player_hit = False
        for (row, col), original_cell in original_cells.items():
            for enemy in enemies:
                if enemy.current_position == (row, col):
                    hit_enemies.append(enemy)

            if player_1.current_position == (row, col):
                player_hit = True

        self.renderer.canvas.after(1000, self.restore_cells, original_cells)
        return hit_enemies, player_hit
    
    def set_renderer(self, renderer):
        self.renderer = renderer
    