import json

class GameState:
    """  
    Representa o estado do jogo e gerencia a leitura e salva a escrita das configurações em gameConfig.json.

    Esta classe permite carregar e salvar os atributos do jogo, fornecendo valores padrão caso o arquivo esteja ausente ou contenha valores inválidos. 
    Todos os atributos têm getters e setters para controle de acesso e atualização dos dados, permite que outras partes do jogo leiam e alterem informações 
    do jogador e do mapa sem manipular diretamente o JSON. Utiliza o método save() para escrever e de fato sobrescrever o JSON.
    
    Attributes:
        rounds_played (int): Número de partidas já jogadas.
        rounds_survived (int): Número de vezes que o jogador já sobreviveu.
        difficulty (str): Dificuldade atual do jogo ('easy', 'medium', 'hard').
        survived_turns (int): Número de turnos sobrevividos na partida atual.
        bombs_utilized (int): Número de bombas utilizadas na partida atual.
        game_over_cause (str): Causa da última morte do jogador.
        game_over_turn (int): Turno em que o jogador morreu na última partida.
        maximum_turn (int): Limite máximo de turnos por partida.
        bomb_range (int): Alcance da bomba em células.
        bomb_timer (int): Quantidade de turnos até a detonação da bomba.
        enemy_start (int): Número inicial de inimigos no mapa.
        enemy_quantity (int): Quantidade atual de inimigos vivos no mapa.
        enemy_spawn_frequency (int): Quantos inimigos vão nascer a cada 5 turnos sobrevividos, é baseado na dificuldade.
        killed_enemies (int): Número de inimigos mortos na partida atual.
        obstacle_destruction_rate (float): Probabilidade de obstáculos destruíveis e indestrutíveis aparecerem no mapass.
    """    

    def __init__(self):
        self.config_path = "config/gameConfig.json"
        self.config = {}

        # Valores padrão para caso JSON falhe
        self.rounds_played = 1
        self.rounds_survived = 1
        self.difficulty = "easy"
        self.survived_turns = 1
        self.bombs_utilized =  0
        self.game_over_cause = "None"
        self.game_over_turn = 0
        self.maximum_turn = 11
        self.bomb_range = 2
        self.bomb_timer = 2
        self.enemy_start = 2
        self.enemy_quantity = 2
        self.enemy_spawn_frequency = 0
        self.killed_enemies = 0
        self.obstacle_destruction_rate = 0.90

    def get_rounds_played(self):
        return self.rounds_played
    
    def set_rounds_played(self, value):
        self.rounds_played = value

    def get_rounds_survived(self):
        return self.rounds_survived
    
    def set_rounds_survived(self, value):
        self.rounds_survived = value

    def get_difficulty(self):
        return self.difficulty
    
    def set_difficulty(self, value):
        self.difficulty = value

    def get_survived_turns(self):
        return self.survived_turns
    
    def set_survived_turns(self,value):
        self.survived_turns = value

    def get_bombs_utilized(self):
        return self.bombs_utilized
    
    def set_bombs_utilized(self, value):
        self.bombs_utilized = value

    def get_game_over_cause(self):
        return self.game_over_cause
    
    def set_game_over_cause(self, value):
        self.game_over_cause = value

    def get_game_over_turn(self):
        return self.game_over_turn
    
    def set_game_over_turn(self, value):
        self.game_over_turn = value

    def get_maximum_turn(self):
        return self.maximum_turn
    
    def set_maximum_turn(self, value):
        self.maximum_turn = value

    def get_bomb_range(self):
        return self.bomb_range
    
    def set_bomb_range(self, value):
        self.bomb_range = value

    def get_bomb_timer(self):
        return self.bomb_timer
    
    def set_bomb_timer(self, value):
        self.bomb_timer = value

    def get_enemy_start(self):
        return self.enemy_start
    
    def set_enemy_start(self, value):
        self.enemy_start = value

    def get_enemy_quantity(self):
        return self.enemy_quantity
    
    def set_enemy_quantity(self, value):
        self.enemy_quantity = value

    def get_enemy_spawn_frequency(self):
        return self.enemy_spawn_frequency
    
    def set_enemy_spawn_frequency(self, value):
        self.enemy_spawn_frequency = value

    def get_killed_enemies(self):
        return self.killed_enemies
    
    def set_killed_enemies(self, value):
        self.killed_enemies = value

    def get_obstacle_destruction_rate(self):
        return self.obstacle_destruction_rate
    
    def set_obstacle_destruction_rate(self, value):
        self.obstacle_destruction_rate = value

    def open(self):
        try:
            with open(self.config_path, "r") as configFile:
                self.config = json.load(configFile)

            self.rounds_played = self.config.get("roundsPlayed", self.rounds_played)
            self.rounds_survived = self.config.get("roundsSurvived", self.rounds_survived)
            self.difficulty = self.config.get("difficulty", self.difficulty)
            self.survived_turns = self.config.get("survivedTurns", self.survived_turns)
            self.bombs_utilized = self.config.get("bombsUtilized", self.bombs_utilized)
            self.game_over_cause = self.config.get("gameOverCause", self.game_over_cause)
            self.game_over_turn = self.config.get("gameOverTurn", self.game_over_turn)
            self.maximum_turn = self.config.get("maximumTurn", self.maximum_turn)
            self.bomb_range = self.config.get("bombRange", self.bomb_range)
            self.bomb_timer = self.config.get("bombTimer", self.bomb_timer)
            self.enemy_start = self.config.get("enemyStart", self.enemy_start)
            self.enemy_quantity = self.config.get("enemyQuantity", self.enemy_quantity)
            self.enemy_spawn_frequency = self.config.get("enemySpawnFrequency", self.enemy_spawn_frequency)
            self.killed_enemies = self.config.get("enemiesKilled", self.killed_enemies)
            self.obstacle_destruction_rate = self.config.get("obstacleDestructionRate", self.obstacle_destruction_rate)

        except FileNotFoundError:
            print("Erro ao abrir arquivo! Arquivo não existe.")
        
    def save(self):
        configs = {
            "roundsPlayed" : self.rounds_played,
            "roundsSurvived" : self.rounds_survived,
            "difficulty" : self.difficulty,
            "survivedTurns" : 0,
            "bombsUtilized" : 0,
            "gameOverCause" : self.game_over_cause,
            "gameOverTurn" : 0,
            "maximumTurn" : self.maximum_turn,
            "bombRange" : self.bomb_range,
            "bombTimer" : self.bomb_timer,
            "enemyStart" : self.enemy_start,
            "enemyQuantity" : self.enemy_quantity,
            "enemySpawnFrequency" : self.enemy_spawn_frequency,
            "enemiesKilled" : self.killed_enemies,
            "obstacleDestructionRate" : self.obstacle_destruction_rate
        }

        with open(self.config_path, "w") as file:
            json.dump(configs, file, indent=4)
