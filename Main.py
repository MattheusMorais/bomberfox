from tkinter import *
from controller.Gameplay import Gameplay
 
def main():
    """ 
    Inicializa e executa o loop principal do jogo.
    """
    window = Tk()
    window.title("BomberFox")
    window.geometry("1920x1080")
    window.minsize(800, 800)
    window.config(bg="black")

    game_frame = Frame(window)
    game_frame.pack(fill=BOTH, expand=True)
 
    game_play = Gameplay(game_frame)
    window.mainloop()

if __name__ == "__main__":
    main()
    