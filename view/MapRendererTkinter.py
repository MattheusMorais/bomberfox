from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

class MapRendererTkinter:

    def __init__(self, map_canvas, hud_canvas, restart_callback, game_state, tile_size=48):
        self.tiles = []
        self.map_canvas = map_canvas
        self.hud_canvas = hud_canvas
        self.game_state = game_state
        self.restart_callback = restart_callback
        self.tile_size = tile_size
        self.BASE_DIR = Path.cwd() / "assets" / "Map"

        def load_map_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            img = img.resize((self.tile_size, self.tile_size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        
        def load_hud_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            img = img.resize((300,580), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        
        def load_button_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            img = img.resize((300, 70), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        
        self.images = {
            "!": load_map_image("floor.png"),
            "#": load_map_image("wall.png"),
            "+": load_map_image("breakable.png"),
            "P": load_map_image("player.png"),
            "E": load_map_image("enemy.png"),
            "B": load_map_image("bomb.png"),
            "*": load_map_image("explosion.png"),
            "HUD": load_hud_image("hud.png"),
            "lower_diff_button": load_button_image("lower_diff_button.png")
        }

        self.hud_canvas.create_image(150, 0, image=self.images["HUD"], anchor="n", tags="bg_hud")
        self.hud_canvas.create_image(145, 515, image=self.images["lower_diff_button"], anchor="n", tags=("hud", "lower_diff_button"))
        self.hud_canvas.tag_bind("lower_diff_button", "<Button-1>", lambda event: self.restart_callback())

        x_pos = 150 

        self.bombs_utilized = self.hud_canvas.create_text(x_pos, 180, text=f"{self.game_state.get_bombs_utilized()}", fill="white", font=("Arial", 35, "bold"), tags="txt_hud")
        self.enemy_quantity = self.hud_canvas.create_text(x_pos, 220, text=f"{self.game_state.get_enemy_quantity()}", fill="white", font=("Arial", 35, "bold"), tags="txt_hud")
        self.survived_turns = self.hud_canvas.create_text(x_pos, 260, text=f"{self.game_state.get_survived_turns()}", fill="white", font=("Arial", 35, "bold"), tags="txt_hud")
        self.maximum_turn = self.hud_canvas.create_text(x_pos, 300, text=f"{self.game_state.get_maximum_turn()}", fill="#ecce32", font=("Arial", 35, "bold"), tags="txt_hud")
        self.killed_enemies = self.hud_canvas.create_text(x_pos, 340, text=f"{self.game_state.get_killed_enemies()}", fill="white", font=("Arial", 35, "bold"), tags="txt_hud")
        self.difficulty = self.hud_canvas.create_text(x_pos, 380, text=f"{self.game_state.get_difficulty().capitalize()}", fill="white", font=("Arial", 35, "bold"), tags="txt_hud")

    def render(self, matrix):
        self.map_canvas.delete("all")
        for row_idx, row in enumerate(matrix):
            for col_idx, symbol in enumerate(row):
                self.draw(row_idx, col_idx, symbol)

        self.hud_canvas.tag_raise("bg_hud")
        self.hud_canvas.tag_raise("txt_hud")
        self.hud_canvas.tag_raise("lower_diff_button")

    def update_cell(self, row, col, symbol):
        self.map_canvas.delete(f"cell_{row}_{col}")
        self.draw(row, col, symbol)

        
 
    def draw(self, row, col, symbol):
        self.map_canvas.delete(f"cell_{row}_{col}")
    
        x = col * self.tile_size
        y = row * self.tile_size

        self.map_canvas.create_image(x, y, anchor="nw", image=self.images["!"], tags=f"cell_{row}_{col}")

        if symbol != "!":
            image = self.images.get(symbol)
            if image:
                self.map_canvas.create_image(x, y, anchor="nw", image=image, tags=f"cell_{row}_{col}")
            else:
                print(f"Aviso: Símbolo '{symbol}' não encontrado no dicionário de imagens!")

    