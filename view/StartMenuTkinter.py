from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

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
        self.background_path = self.BASE_DIR / "startMenu_bg1.png"
        self.background_image = PhotoImage(file=self.background_path)
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

        if self.game_state.get_rounds_played() > 0:
            self.stats_path = self.BASE_DIR / "stats.png"
            self.stats_image = Image.open(self.stats_path).resize((400,650), Image.Resampling.NEAREST)

            alpha = self.stats_image.getchannel("A")
            alpha = alpha.point(lambda p: int(p * 0.90))
            self.stats_image.putalpha(alpha)

            self.stats_image = ImageTk.PhotoImage(self.stats_image)
            self.canvas.create_image(230, 380, image=self.stats_image, tags="stats")

            self.rounds_played_path = self.BASE_DIR / "rounds_played.png"
            self.rounds_played_image = Image.open(self.rounds_played_path).resize((200,100), Image.Resampling.NEAREST)
            self.rounds_played_image = ImageTk.PhotoImage(self.rounds_played_image)
            self.canvas.create_image(230,170, image=self.rounds_played_image, tags="stats")
            self.canvas.create_text(
                230, 250, #350
                text=f"{self.game_state.get_rounds_played()}",
                font=("Arial", 35, "bold"),
                fill="#ecce32"
            )

            self.gameover_cause_path = self.BASE_DIR / "sem_titulo1.png"
            self.gameover_cause_image = Image.open(self.gameover_cause_path).resize((250,100), Image.Resampling.NEAREST)
            self.gameover_cause_image = ImageTk.PhotoImage(self.gameover_cause_image)   
            self.canvas.create_image(230,350, image=self.gameover_cause_image, tags="stats")         
            self.canvas.create_text(
                230, 430,
                text=f"{self.game_state.get_game_over_cause()}",
                tags="stats",
                font=("Arial", 40, "bold"),
                fill="#ecce32"
            )

            self.killed_enemies_path = self.BASE_DIR / "killed_enemies.png"
            self.killed_enemies_image = Image.open(self.killed_enemies_path).resize((250,100), Image.Resampling.NEAREST)
            self.killed_enemies_image = ImageTk.PhotoImage(self.killed_enemies_image)
            self.canvas.create_image(230,540, image=self.killed_enemies_image, tags="stats")         

            self.canvas.create_text(
                230, 630,
                text=f"{self.game_state.get_killed_enemies()}",
                tags="stats",
                font=("Arial", 40, "bold"),
                fill="#ecce32"
            )

            self.play_button()

    def on_play_click(self, event=None):
        self.canvas.destroy()
        self.start_game()

    def play_button(self):
        self.play_button_path = self.BASE_DIR / "play_button.png"
        self.play_button_image = Image.open(self.play_button_path).resize((250,200), Image.Resampling.NEAREST)
        self.play_button_image = ImageTk.PhotoImage(self.play_button_image)
        self.button = self.canvas.create_image(1120, 370, image=self.play_button_image, tags="play")
        self.canvas.tag_bind(self.button, "<Button-1>", self.on_play_click)
        
