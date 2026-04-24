from model.Helper import clear_screen
from tkinter import *
from controller.Gameplay import Gameplay

def main():
    """ 
    Inicializa e executa o loop principal do jogo.

    Observação: O loop while True garante que o jogador possa reiniciar o jogo sem que a execução anterior continue em segundo plano.

    """
    window = Tk()
    window.title("BomberBoy")
    window.geometry("800x800")
    window.minsize(400, 300)

    game_play = Gameplay(window)
    window.mainloop()
    game_play.game_loop()

if __name__ == "__main__":
    clear_screen() 
    main()
