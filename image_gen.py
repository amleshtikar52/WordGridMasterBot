from PIL import Image, ImageDraw, ImageFont

def generate_image(grid, words, found):
    size = len(grid)
    img = Image.new("RGB", (600, 700), "#111111")
    d = ImageDraw.Draw(img)

    cell = 40
    x0, y0 = 50, 50

    for i in range(size):
        for j in range(size):
            d.rectangle(
                [x0+j*cell, y0+i*cell, x0+(j+1)*cell, y0+(i+1)*cell],
                outline="white"
            )
            d.text(
                (x0+j*cell+12, y0+i*cell+8),
                grid[i][j],
                fill="white"
            )

    y_words = y0 + size*cell + 20
    for w in words:
        status = "✅" if w in found else "❌"
        d.text((50, y_words), f"{status} {w[0].upper()}-- ({len(w)})", fill="white")
        y_words += 30

    return img
