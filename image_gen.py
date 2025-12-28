from PIL import Image, ImageDraw
import random
import io

def generate_image(grid_size, words):
    img = Image.new("RGB", (720, 900), "white")
    draw = ImageDraw.Draw(img)

    cell = 50
    sx, sy = 40, 40

    letters = [chr(random.randint(65, 90)) for _ in range(grid_size * grid_size)]
    i = 0

    for r in range(grid_size):
        for c in range(grid_size):
            x = sx + c * cell
            y = sy + r * cell
            draw.rectangle([x, y, x+cell, y+cell], outline="black")
            draw.text((x+18, y+12), letters[i], fill="black")
            i += 1

    y = sy + grid_size * cell + 30
    draw.text((40, y), "🔥 WORD GRID CHALLENGE 🔥", fill="black")
    y += 40

    draw.text((40, y), "Find these words:", fill="black")
    y += 30

    for w in words:
        hint = w[0] + "-" * (len(w)-1)
        draw.text((40, y), f"{hint} ({len(w)})", fill="black")
        y += 25

    y += 20
    draw.text((40, y), "Type the words you find to score points!", fill="black")

    bio = io.BytesIO()
    bio.name = "wordgrid.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio
