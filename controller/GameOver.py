from view.GameOverTkinter import GameOverTkinter

class GameOver:
    """ 
    Exibe a tela de fim de jogo, gerenciando a causa e o turno final.   

    Attributes:
        CAUSE_EXPLOSION (str): Representa morte por explosão.
        CAUSE_ENEMY (str): Representa morte por inimigo.
        CAUSE_SUCCESS (str): Representa sucesso em sobreviver.
        game_over_cause (str): Causa do fim do jogo.
        game_over_turn (int): Turno em que o jogador foi eliminado ou sobreviveu.
        GameOverTkinter (GameOverTkinter): Instância da interface gráfica para exibir a tela de fim de jogo.
    """

    CAUSE_EXPLOSION = "Explosão"
    CAUSE_ENEMY = "Inimigo"
    CAUSE_SUCCESS = "Sobreviveu!"

    def __init__(self, game_over_cause, game_over_turn, game_over_canva):
        self.game_over_cause = game_over_cause
        self.game_over_turn = game_over_turn
        self.game_over_canva = game_over_canva
        GameOverTkinter(game_over_cause, game_over_turn, game_over_canva)
        