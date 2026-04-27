from tkinter import *
from pathlib import Path

class StartMenuTkinter:

    def __init__(self, game_state, window, start_game):
        self.window = window
        self.game_state = game_state
        self.start_game = start_game
        self.BASE_DIR = Path.cwd() / "assets" / "StartMenu"
        self.canvas = Canvas(self.window)
        self.canvas.pack(fill="both", expand=True)
        self.show_welcome()

    def show_welcome(self):
        
        self.background_path = self.BASE_DIR / "startMenu_bg.png"
        self.background_image = PhotoImage(file=self.background_path).subsample(4,4)

        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

        self.canvas.create_text(400, 80, text="BOMBERBOY", font=("Arial", 40), fill="white")

        if self.game_state.get_rounds_played() > 0:
            self.mid_box_path = self.BASE_DIR / "mid_box.png"
            self.mid_box_image = PhotoImage(file=self.mid_box_path).subsample(3,3)
            
            self.canvas.create_image(403, 380, image=self.mid_box_image, tags="mid_box")
            self.canvas.create_text(400, 150, 
                            text="ESTATÍSTICAS DA ÚLTIMA SESSÃO", 
                            tags="mid_box",
                            font=("Arial", 16, "bold"),
                            fill="white"
                            )
            self.canvas.create_text(215, 290,
                            text="PARTIDAS", 
                            font=("Arial", 18), 
                            tags="mid_box",
                            fill="white"
                            )
            self.canvas.create_text(215, 310, 
                            text="JOGADAS", 
                            font=("Arial", 18), 
                            tags="mid_box",
                            fill="white"
                            )
            self.canvas.create_text(
                220, 350, #350
                text=f"{self.game_state.get_rounds_played()}",
                font=("Arial", 35, "bold"),
                fill="#ecce32"
            )
            self.canvas.create_text(405, 290, 
                            text="ÚLTIMA",
                            tags="mid_box",
                            font=("Arial", 18), 
                            fill="white"
                            )
            self.canvas.create_text(405, 310, 
                            text="ELIMINAÇÃO",
                            tags="mid_box",
                            font=("Arial", 18), 
                            fill="white"
                            )
            self.canvas.create_text(
                405, 350,
                text=f"{self.game_state.get_game_over_cause()}",
                tags="mid_box",
                font=("Arial", 20, "bold"),
                fill="#ecce32"
            )
            self.canvas.create_text(595, 290, 
                            text="INIMIGOS",
                            tags="mid_box",
                            font=("Arial", 18), 
                            fill="white"
                            )
            self.canvas.create_text(595, 310, 
                            text="ELIMINADOS",
                            tags="mid_box",
                            font=("Arial", 18), 
                            fill="white"
                            )
            self.canvas.create_text(
                595, 350,
                text=f"{self.game_state.get_killed_enemies()}",
                tags="mid_box",
                font=("Arial", 35, "bold"),
                fill="#ecce32"
            )

            self.play_button()

        else:
            self.canvas.create_text(400,400,text="\nPrimeira partida! Boa sorte.\n", font=("Arial",40), fill="white")
            self.play_button()
    
    def on_play_click(self, event=None):
        self.canvas.destroy()
        self.start_game()

    def play_button(self):
        self.play_button_path = self.BASE_DIR / "play_button.png"
        self.play_button_image = PhotoImage(file=self.play_button_path).subsample(5,5)
        
        self.button = self.canvas.create_image(400, 680, image=self.play_button_image, tags="play")
        self.canvas.tag_bind(self.button, "<Button-1>", self.on_play_click)
        
