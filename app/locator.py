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
    files = os.listdir(tmp_dir)
    for f in files:
        os.remove(f"{tmp_dir}/{f}")
    images = split(img)
    for i in range(len(images)):
        images[i].save(f"{tmp_dir}/{i}.png")
    test = ImageList.from_folder(tmp_dir)
    learn.data.add_test(test)
    preds = learn.get_preds(ds_type=DatasetType.Test)
    classes = learn.data.classes

    # Identify the grids which are player squares
    for i in range(len(preds[0])):
        max_class = "terrain"
        max_score = 0
        for j in range(len(preds[0][i])):
            if preds[0][i][j] > max_score:
                max_class = classes[j]
                max_score = preds[0][i][j]
        if max_class == "terrain":
            continue
        num = int(test.items[i].stem)
        row = num // 15
        column = num % 15
        tags.append(f"{column};{row};{max_class}")

    tags.sort()
    return " ".join(tags)


def create_composite(previous_positions, img):
    print(previous_positions)
    grid_size = 10
    overlay = PIL.Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = PIL.ImageDraw.Draw(overlay)

    num_positions = len(previous_positions)
    for i in range(num_positions):
        grid = previous_positions[i]
        grid = grid.split(" ")
        grid = [g.split(";") for g in grid]
        grid = [(int(g[0]), int(g[1]), g[2]) for g in grid]

        alpha = int(128 * i/num_positions)
        for l in grid:
            fill = (255, 0, 255, alpha)
            if l[2] == "blue":
                fill = (0, 255, 255, alpha)
            if l[2] == "blue-red":
                fill = (255, 255, 0, alpha)

            x1 = l[0] * grid_size
            x2 = x1 + grid_size
            y1 = l[1] * grid_size
            y2 = y1 + grid_size

            p1 = (x1, y1)
            p2 = (x2, y2)

            draw.line([p1, p2], fill=fill, width=2)

    out = PIL.Image.alpha_composite(img, overlay)
    return out
