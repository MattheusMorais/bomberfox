from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

class StartMenuTkinter:
    def __init__(self, game_state, game_frame, start_game):
        self.game_frame = game_frame
        self.game_state = game_state
        self.start_game = start_game
        self.BASE_DIR = Path.cwd() / "assets" / "StartMenu"
        
        self.startMenu_canvas = Canvas(self.game_frame, highlightthickness=0)
        self.startMenu_canvas.pack(fill="both", expand=True)

        self.w = self.game_frame.winfo_toplevel().winfo_width()
        self.h = self.game_frame.winfo_toplevel().winfo_height()

        if self.w < 100:
            self.w, self.h = 1920, 1080

        self.show_welcome()

    def show_welcome(self):
        self.background_path = self.BASE_DIR / "startMenu_bg1.png"
        self.background_image = Image.open(self.background_path).resize((self.w, self.h), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.startMenu_canvas.create_image(0, 0, image=self.background_image, anchor=NW)

        if self.game_state.get_rounds_played() > 0:
            self.stats_path = self.BASE_DIR / "stats.png"
            self.stats_image = Image.open(self.stats_path).resize((600, self.h - 200), Image.Resampling.NEAREST)

            alpha = self.stats_image.getchannel("A")
            alpha = alpha.point(lambda p: int(p * 0.90))
            self.stats_image.putalpha(alpha)
            self.stats_image = ImageTk.PhotoImage(self.stats_image)
            self.startMenu_canvas.create_image(330, self.h // 2, image=self.stats_image, tags="stats")

            self.rounds_played_path = self.BASE_DIR / "rounds_played.png"
            self.rounds_played_image = Image.open(self.rounds_played_path).resize((200, 100), Image.Resampling.NEAREST)
            self.rounds_played_image = ImageTk.PhotoImage(self.rounds_played_image)
            self.startMenu_canvas.create_image(330, 230, image=self.rounds_played_image, tags="stats")
            
            self.startMenu_canvas.create_text(
                330, 330,
                text=f"{self.game_state.get_rounds_played()}",
                font=("Arial", 35, "bold"),
                fill="#ecce32", tags="stats"
            )

            self.gameover_cause_path = self.BASE_DIR / "gameover_cause.png"
            self.gameover_cause_image = Image.open(self.gameover_cause_path).resize((250, 100), Image.Resampling.NEAREST)
            self.gameover_cause_image = ImageTk.PhotoImage(self.gameover_cause_image)   
            self.startMenu_canvas.create_image(330, 480, image=self.gameover_cause_image, tags="stats")         
            
            self.startMenu_canvas.create_text(
                330, 580,
                text=f"{self.game_state.get_game_over_cause()}",
                font=("Arial", 40, "bold"),
                fill="#ecce32", tags="stats"
            )

            self.killed_enemies_path = self.BASE_DIR / "killed_enemies.png"
            self.killed_enemies_image = Image.open(self.killed_enemies_path).resize((250, 100), Image.Resampling.NEAREST)
            self.killed_enemies_image = ImageTk.PhotoImage(self.killed_enemies_image)
            self.startMenu_canvas.create_image(330, 740, image=self.killed_enemies_image, tags="stats")         

            self.startMenu_canvas.create_text(
                330, 840,
                text=f"{self.game_state.get_killed_enemies()}",
                font=("Arial", 40, "bold"),
                fill="#ecce32", tags="stats"
            )

            self.play_button()

    def on_play_click(self, event=None):
        self.startMenu_canvas.destroy()
        self.start_game()

    def play_button(self):
        self.play_button_path = self.BASE_DIR / "play_button.png"
        self.play_button_image = Image.open(self.play_button_path).resize((400, 300), Image.Resampling.NEAREST)
        self.play_button_image = ImageTk.PhotoImage(self.play_button_image)
        self.button = self.startMenu_canvas.create_image(self.w - 400, self.h // 2, image=self.play_button_image, tags="play")
        self.startMenu_canvas.tag_bind(self.button, "<Button-1>", self.on_play_click)