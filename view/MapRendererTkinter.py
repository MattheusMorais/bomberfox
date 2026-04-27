from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

class MapRendererTkinter:

    def __init__(self, canvas, tile_size=48):
        self.tiles = []
        self.canvas = canvas
        self.tile_size = tile_size
        self.BASE_DIR = Path.cwd() / "assets" / "Map"

        def load_image(image_name):
            img = Image.open(self.BASE_DIR / image_name)
            
            img = img.resize((self.tile_size, self.tile_size), Image.Resampling.NEAREST)
            return ImageTk.PhotoImage(img)

        self.images = {
            "!": load_image("floor.png"),
            "#": load_image("wall.png"),
            "+": load_image("breakable.png"),
            "P": load_image("player.png"),
            "E": load_image("enemy.png"),
            "B": load_image("bomb.png")
        }

    def render(self, matrix):
        self.canvas.delete("all")
        for row_idx, row in enumerate(matrix):
            for col_idx, symbol in enumerate(row):
                self.draw(row_idx, col_idx, symbol)
 
    def update_cell(self, row, col, symbol):
        self.canvas.delete(f"cell_{row}_{col}")
        self.draw(row, col, symbol)
 
    def draw(self, row, col, symbol):
        self.canvas.delete(f"cell_{row}_{col}")
    
        x = col * self.tile_size
        y = row * self.tile_size

        self.canvas.create_image(x, y, anchor="nw", image=self.images["!"], tags=f"cell_{row}_{col}")

        if symbol != " ":
            image = self.images.get(symbol)
            if image:
                self.canvas.create_image(x, y, anchor="nw", image=image, tags=f"cell_{row}_{col}")   