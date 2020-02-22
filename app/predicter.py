from PIL import Image, ImageDraw
from fastai.basic_train import load_learner
from io import BytesIO

from fastai.vision import open_image

learn = load_learner("./app/models", "predict.pth")


def predict_locations(aug_map):
    imgByteArr = BytesIO()
    aug_map.save(imgByteArr, format='PNG')
    # lolmap.save("/home/isaac/dev/league/lol-web-server/app/composite.png")

    fai_img = open_image(imgByteArr)
    img_classes = learn.data.classes
    predictions = learn.predict(fai_img)[2]
    preds = []
    for i in range(len(predictions)):
        if predictions[i] > 0.2:
            preds.append(img_classes[i])
    preds = [[int(p.split(";")[0]), int(p.split(";")[1])] for p in preds]

    return preds


def draw_grid(draw, labels, grid_mult):
    grid = 5 * grid_mult
    fill = (255, 255, 255, 96)
    for l in labels:
        x = l[0] * grid - 10
        y = l[1] * grid + 15
        draw.rectangle((x, y, x + grid, y + grid), fill=fill)