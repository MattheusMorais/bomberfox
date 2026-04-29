import os
import sys
from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path

class GameOverTkinter:
    """Interface visual do Game Over utilizando Tkinter e PIL."""

    def __init__(self, game_over_cause, game_over_turn, game_over_canvas):
        self.game_over_cause = game_over_cause
        self.game_over_turn = game_over_turn
        self.game_over_canvas = game_over_canvas
        self.BASE_DIR = Path.cwd() / "assets" / "GameOver"

        w = self.game_over_canvas.winfo_width()
        h = self.game_over_canvas.winfo_height()

        if w < 100: 
            w = 1920
            h = 1080

        def load_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        
        def load_button_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            img = img.resize((300, 150), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        
        self.images = {
            "killed_by_bomb": load_image("killed_by_bomb.png"),
            "killed_by_enemy": load_image("killed_by_enemy.png"),
            "survived": load_image("survived.png"),
            "restart_button": load_button_image("restart_button.png")
        }

        self.game_over_canvas.image_refs = self.images

        if self.game_over_cause == "Sobreviveu!":
            self.game_over_canvas.create_image(0, 0, image=self.images["survived"], anchor="nw", tags="game_over")        
        elif self.game_over_cause == "Explosão":
            self.game_over_canvas.create_image(0, 0, image=self.images["killed_by_bomb"], anchor="nw", tags="game_over")
        elif self.game_over_cause == "Inimigo":
            self.game_over_canvas.create_image(0, 0, image=self.images["killed_by_enemy"], anchor="nw", tags="game_over")

        self.game_over_canvas.create_text(
            1540, 850, 
            text=f"{self.game_over_turn}", 
            font=("Arial", 50, "bold"), 
            fill="#ecce32",
            tags="game_over" 
        )

        def on_restart_click(event):
            os.execl(sys.executable, sys.executable, *sys.argv)
        
        self.restart_button = self.game_over_canvas.create_image(670, 920, image=self.images["restart_button"], tags="game_over")
        self.game_over_canvas.tag_bind(self.restart_button, "<Button-1>", on_restart_click)
