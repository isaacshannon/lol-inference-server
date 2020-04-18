from PIL import Image, ImageDraw
from fastai.basic_train import load_learner
from io import BytesIO

from fastai.vision import open_image

learn = load_learner("./app/models", "predict_18_apr_2020.pth")


def predict_locations(aug_map):
    imgByteArr = BytesIO()
    aug_map.save(imgByteArr, format='PNG')

    fai_img = open_image(imgByteArr)
    img_classes = learn.data.classes
    predictions = learn.predict(fai_img)[2]
    preds = []
    for i in range(len(predictions)):
        if predictions[i] > 0.05:
            preds.append(f"{img_classes[i]};{predictions[i]}")

    preds = [[int(p.split(";")[0]), int(p.split(";")[1]), p.split(";")[2], float(p.split(";")[3])] for p in preds]

    return preds


def draw_grid(draw, labels):
    grid = 15
    fill = (255, 255, 255, 96)
    for l in labels:
        x = l[0] * grid - 10
        y = l[1] * grid + 15
        if l[2] == "r":
            draw.rectangle((x, y, x + grid, y + grid), fill=fill)