from PIL import Image, ImageDraw
from fastai import *
from fastai.vision import *
from io import BytesIO
import time

learn = load_learner("/home/isaac/dev/league/lol-web-server/app/models", "locator.pth")
height = 10
width = 10
padding = 10


# The splitter separates the images which have player locator into 10x10px images for training.
def split(img):
    images = []

    img_width, img_height = img.size
    for i in range(0, img_height, height):
        for j in range(0, img_width, width):
            box = (j - padding, i - padding, j + width + padding, i + height + padding)
            a = img.crop(box)
            images.append(a)

    return images


def locate_players(img):
    tags = []

    # Predict the grid image types
    tmp_dir = "/home/isaac/dev/league/lol-web-server/app/tmp"
    images = split(img)
    for i in range(len(images)):
        images[i].save(f"{tmp_dir}/{i}.png")
    test = ImageList.from_folder(tmp_dir)
    learn.data.add_test(test)
    preds = learn.get_preds(ds_type=DatasetType.Test)

    # Identify the grids which are player squares
    prediction_threshold = 0.5
    row = 0
    column = 0
    for i in range(len(preds[0])):
        if preds[0][i][1] > prediction_threshold:
            tags.append(f"{row}-{column}")
            num = int(test.items[i].stem)
            row = num // 15
            column = num % 15
            tags.append(f"{column}-{row}")

    tags.sort()
    return " ".join(tags)


def create_composite(previous_positions, img):
    grid_size = 10
    overlay = PIL.Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = PIL.ImageDraw.Draw(overlay)

    for i in range(len(previous_positions)):
        grid = previous_positions[i]
        grid = grid.split(" ")
        grid = [(int(g.split("-")[0]), int(g.split("-")[1])) for g in grid]

        c1 = int(255 * ((1 + i) / 16))
        c2 = 255 - c1
        alpha = 128
        fill = (128, 0, c2, alpha)
        for l in grid:
            x = l[0] * grid_size
            y = l[1] * grid_size
            draw.line([(x, y), (x + grid_size, y + grid_size)], fill=fill, width=2)

    out = PIL.Image.alpha_composite(img, overlay)
    return out
