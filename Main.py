from tkinter import *
from controller.Gameplay import Gameplay
 
def main():
    """ 
    Inicializa e executa o loop principal do jogo.
    """
    window = Tk()
    window.title("BomberBoy")
    window.geometry("1000x1000")
    window.minsize(400, 300)
 
    game_play = Gameplay(window)
    window.mainloop()
 
if __name__ == "__main__":
    main()
    