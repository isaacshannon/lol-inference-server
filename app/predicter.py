from PIL import Image, ImageDraw
from fastai.basic_train import load_learner
from io import BytesIO

from fastai.vision import open_image

learn = load_learner("/home/isaac/dev/league/lol-web-server/app/models", "predict.pth")


def predict_locations(aug_map, og_map):
    grid_size = og_map.size[0]//15
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
    preds = [(int(p.split(";")[0]), int(p.split(";")[1]), p.split(";")[2]) for p in preds]
    overlay = Image.new('RGBA', og_map.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw_grid(draw, preds, grid_size)
    out = Image.alpha_composite(og_map, overlay)

    return out

def draw_grid(draw, labels, grid_size):
    for l in labels:
        fill = (0, 0, 255, 96)
        if l[2] == "red":
            fill = (255, 0, 0, 96)
        if l[2] == "blue-red":
            fill = (255, 255, 0, 96)
        x = l[0] * grid_size
        y = l[1] * grid_size
        draw.rectangle((x, y, x + grid_size, y + grid_size), fill=fill)