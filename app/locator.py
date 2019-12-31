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
    start = time.time()
    images = split(img)
    predictions = []
    for im in images:
        imgByteArr = BytesIO()
        im.save(imgByteArr, format='PNG')
        fai_img = open_image(imgByteArr)
        prediction = str(learn.predict(fai_img)[0])
        predictions.append(prediction)

    row = 0
    column = 0
    for i in range(len(predictions)):
        if predictions[i] == "player":
            tags.append(f"{column}-{row}")
        column += 1
        if column >= 15:
            row += 1
            column = 0

    tags.sort()
    print(tags)
    print(time.time() - start)
    return " ".join(tags)

def overlay