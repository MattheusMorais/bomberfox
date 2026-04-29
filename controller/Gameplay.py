import sys
import os
import random
from tkinter import *
from model.Enemy import Enemy
from model.Map import Map
from model.Obstacles import Obstacles
from model.Player import Player
from service.GameState import GameState
from view.GameOver import GameOver
from view.StartMenuTkinter import StartMenuTkinter
from view.MapRendererTkinter import MapRendererTkinter

class Gameplay:
    """
    Controla toda a lógica do jogo: inicialização, loop principal, inimigos, 
    bombas, jogador, dificuldade e Game Over.

    Attributes:
        game_state (GameState): Instância que mantém o estado do jogo.
        start_menu (StartMenuTkinter): Menu inicial com estatísticas anteriores.
        enemies_killed (int): Contador de inimigos eliminados na partida atual.
        initial_number_of_enemies (int): Número de inimigos ao iniciar a partida.
        enemies (list): Lista de inimigos ativos no mapa.
        start_game_map: Instância do mapa do jogo.
        free_positions (list): Posições livres no mapa para spawn de inimigos.
        player_1: Instância do jogador.
    """

    def __init__(self, game_frame):
        self.game_frame = game_frame
        self.window = game_frame.winfo_toplevel()
        self.game_state = GameState()
        self.game_state.open()

        self.binds = {
            "move_up": self.window.bind("<w>",lambda event: self.player_1.move('w', self.start_game_map)),
            "move_down": self.window.bind("<s>",lambda event: self.player_1.move('s', self.start_game_map)),
            "move_left": self.window.bind("<a>",lambda event: self.player_1.move('a', self.start_game_map)),
            "move_right": self.window.bind("<d>",lambda event: self.player_1.move('d', self.start_game_map)),
            "quit": self.window.bind("<q>", lambda event: self.close_game()),
            "put_bomb": self.window.bind("<f>",lambda event: self.player_1.put_bomb('f', self.start_game_map)),
        }

        self.start_menu = StartMenuTkinter(
            self.game_state,
            self.game_frame,
            self.start_game
        )
 
        self.enemies_killed = 0
        self.initial_number_of_enemies = self.game_state.get_enemy_start()
        self.game_state.set_enemy_quantity(self.initial_number_of_enemies)
        self.game_state.set_game_over_cause("None")
        self.enemies = []
 
        self.map_canvas = None
        self.renderer = None

    def setup_map(self):
        """Inicializa o mapa, canvas e renderer."""
        self.start_game_map = Map(self.game_state)
        self.free_positions = self.start_game_map.get_free_positions()

        container = Frame(self.game_frame, bg="#000000")
        container.pack(expand=True)

        map_size = self.start_game_map.size * 48
        self.map_canvas = Canvas(container, width=map_size, height=map_size, bg="#653c08", highlightthickness=0)
        self.map_canvas.grid(row=0, column=0, sticky="nsew")

        self.hud_canvas = Canvas(container, width=300, height=map_size, bg="#2c3e50", highlightthickness=0)
        self.hud_canvas.grid(row=0, column=1, sticky="nsew")

        self.renderer = MapRendererTkinter(self.map_canvas, self.hud_canvas, self.lower_difficulty, self.game_state)
        self.start_game_map.set_renderer(self.renderer)
 
        self.player_1 = Player(self.game_state)
        Obstacles(self.game_state)
        self.create_start_enemies()

        self.renderer.render(self.start_game_map.matrix)

    def game_loop(self):
        if self.player_1.is_alive() and self.game_state.get_game_over_cause() == "None":
            if self.player_1.moved:
                self.update_bombs()
                self.create_dynamic_enemies()
                self.update_enemies()

                self.renderer.render(self.start_game_map.matrix)
                self.player_1.moved = False
            
            self.game_frame.after(100, self.game_loop)

            if not self.player_1.is_alive():
                self.update_rounds_played()
                self.game_state.save()
                
            if self.game_state.get_survived_turns() >= self.game_state.get_maximum_turn():
                self.update_rounds_played()
                self.update_rounds_survived()
                self.update_difficulty()
                    
                self.player_survived()
                self.game_state.save() 

    def close_game(self):
        self.window.destroy()

    def lower_difficulty(self):
        self.lower_difficulty_to_easy()
        self.game_state.save()
        os.execl(sys.executable, sys.executable, *sys.argv) # Reinicia o jogo para aplicar as mudanças de dificuldade

    def create_start_enemies(self):
        for _ in range(self.initial_number_of_enemies):
            free_position = random.choice(self.free_positions)
            self.free_positions.remove(free_position)
            enemy = Enemy(free_position)
            self.enemies.append(enemy)
            row, col = free_position
            self.start_game_map.matrix[row][col] = enemy.SYMBOL
            self.start_game_map.update_cell(row, col, enemy.SYMBOL)

        self.renderer.render(self.start_game_map.matrix)
        
    def create_dynamic_enemies(self):
        if self.game_state.get_survived_turns() % 5 == 0:
            self.update_enemy_spawn_frequency()
            enemies_spawned = []

            enemies_to_spawn = self.game_state.get_enemy_spawn_frequency()
            for _ in range(enemies_to_spawn):
                free_position = random.choice(self.free_positions)
                self.free_positions.remove(free_position)
                enemy = Enemy(free_position)
                enemies_spawned.append(enemy)
                self.enemies.append(enemy)
                row, col = free_position
                self.start_game_map.update_cell(row, col, enemy.SYMBOL)
            
            enemies_quantity = self.game_state.get_enemy_quantity()
            self.game_state.set_enemy_quantity(enemies_quantity + len(enemies_spawned))

            self.renderer.render(self.start_game_map.matrix)

    def update_rounds_played(self):
        rounds_played = self.game_state.get_rounds_played()
        self.game_state.set_rounds_played(rounds_played+1)

    def update_rounds_survived(self):
        rounds_survived = self.game_state.get_rounds_survived()
        self.game_state.set_rounds_survived(rounds_survived+1)
        
    def update_difficulty(self):
        if self.game_state.get_rounds_survived() >= 6:
            self.game_state.set_difficulty("hard")

        elif self.game_state.get_rounds_survived() >= 3:
            self.game_state.set_difficulty("medium")
        
        self.update_bomb_timer()
        self.update_bomb_range()
        self.update_obstacles_proportion_rate()
        self.update_initial_enemies()
        self.update_maximum_turn_limit()

    def lower_difficulty_to_easy(self):
        self.game_state.set_rounds_survived(0)
        self.game_state.set_difficulty("easy")
        self.game_state.set_maximum_turn(15)
        self.game_state.set_bomb_range(1)
        self.game_state.set_bomb_timer(5)
        self.game_state.set_enemy_start(5)
        self.game_state.set_enemy_spawn_frequency(1)
        self.game_state.set_obstacle_destruction_rate(0.9)

    def update_bomb_timer(self):
        difficulty = self.game_state.get_difficulty()

        if difficulty == "hard":
            self.game_state.set_bomb_timer(3)
        
        elif difficulty == "medium":
            self.game_state.set_bomb_timer(4)

    def update_bomb_range(self):
        difficulty = self.game_state.get_difficulty()

        if difficulty == "hard":
            self.game_state.set_bomb_range(3)
        
        elif difficulty == "medium":
            self.game_state.set_bomb_range(2)

    def update_obstacles_proportion_rate(self):
        difficulty = self.game_state.get_difficulty()

        if difficulty == "hard":
            self.game_state.set_obstacle_destruction_rate(0.30)
        
        elif difficulty == "medium":
            self.game_state.set_obstacle_destruction_rate(0.50)

    def update_initial_enemies(self):
        difficulty = self.game_state.get_difficulty()

        if difficulty == "hard":
            self.game_state.set_enemy_start(15)
        
        elif difficulty == "medium":
            self.game_state.set_enemy_start(10)

    def update_maximum_turn_limit(self):
        difficulty = self.game_state.get_difficulty()

        if difficulty == "hard":
            self.game_state.set_maximum_turn(35)
        
        elif difficulty == "medium":
            self.game_state.set_maximum_turn(25)

    def update_enemy_spawn_frequency(self):
        difficulty = self.game_state.get_difficulty()
        if difficulty == "hard":
            self.game_state.set_enemy_spawn_frequency(4)
        
        elif difficulty == "medium":
            self.game_state.set_enemy_spawn_frequency(2)
        
    def update_bombs(self):
        player_hit = False
        hit_enemies = []

        for bomb in self.player_1.active_bombs[:]:
            if bomb.tick():
                hit_enemies, player_hit = self.start_game_map.chain_explosion(bomb, self.player_1, self.enemies)
                self.player_1.active_bombs.remove(bomb)

            if player_hit: # Fim do jogo
                self.player_dead_by_explosion()

        self.renderer.render(self.start_game_map.matrix)
        self.update_enemies_quantity(hit_enemies)

    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.move(self.start_game_map):
                self.player_killed_by_enemy()
                self.player_1.player_alive = False
                
        self.renderer.render(self.start_game_map.matrix)

    def create_game_over_canvas(self):  
        self.game_over_canvas = Canvas(self.window, bg="#000000", highlightthickness=0)
        self.game_over_canvas.pack(fill="both", expand=True)
        return self.game_over_canvas

    def player_survived(self):
        self.game_state.set_game_over_cause(GameOver.cause_SUCCESS)

        game_over_cause = self.game_state.get_game_over_cause()
        game_over_turn = self.game_state.get_survived_turns()
        self.game_state.save()

        self.game_frame.destroy()
        GameOver(game_over_cause, game_over_turn, self.create_game_over_canvas())

    def player_killed_by_enemy(self):
        self.game_state.set_game_over_cause(GameOver.cause_ENEMY)
        self.game_state.set_game_over_turn(self.game_state.get_survived_turns())
        self.player_1.player_alive = False

        game_over_cause = self.game_state.get_game_over_cause()
        game_over_turn = self.game_state.get_game_over_turn()
        self.game_state.save()

        self.game_frame.destroy()
        GameOver(game_over_cause, game_over_turn, self.create_game_over_canvas())
        
    def player_dead_by_explosion(self):
        self.game_state.set_game_over_cause(GameOver.cause_EXPLOSION)
        self.game_state.set_game_over_turn(self.game_state.get_survived_turns())
        self.player_1.player_alive = False

        game_over_cause = self.game_state.get_game_over_cause()
        game_over_turn = self.game_state.get_game_over_turn()
        self.game_state.save()

        self.game_frame.destroy()
        GameOver(game_over_cause, game_over_turn, self.create_game_over_canvas())
        
    def update_enemies_quantity(self, hit_enemies):
        for enemy in self.enemies[:]: 
                if enemy in hit_enemies:
                    self.enemies.remove(enemy)
                    self.enemies_killed += 1
                    enemy_quantity = self.game_state.get_enemy_quantity()
                    self.game_state.set_enemy_quantity(enemy_quantity - 1)
        
        self.game_state.set_killed_enemies(self.enemies_killed)

    def start_game(self):
        self.setup_map()
        self.game_loop()
