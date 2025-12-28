from PIL import Image, ImageDraw, ImageFont
import io


def generate_grid_image(grid):
    size = len(grid)
    cell = 70
    pad = 20

    img_size = size * cell + pad * 2
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    for r in range(size):
        for c in range(size):
            x1 = pad + c * cell
            y1 = pad + r * cell
            x2 = x1 + cell
            y2 = y1 + cell

            draw.rectangle([x1, y1, x2, y2], outline="black", width=2)

            letter = grid[r][c]
            w, h = draw.textsize(letter, font=font)
            draw.text(
                (x1 + (cell - w) / 2, y1 + (cell - h) / 2),
                letter,
                fill="black",
                font=font
            )

    bio = io.BytesIO()
    img.save(bio, "PNG")
    bio.seek(0)
    return bio
