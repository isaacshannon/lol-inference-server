from PIL import Image
from fastai import *
from fastai.vision import *
from io import BytesIO
import time

learn = load_learner("/home/isaac/dev/league/lol-web-server/app/models", "minimap.pth")
height = 10
width = 10
padding = 10

x_coord = None
y_coord = None

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


def predict_img(img):
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='PNG')
    fai_img = open_image(imgByteArr)
    prediction = learn.predict(fai_img)[0]
    return str(prediction)


def predict_x_coord(img):
    img_width, img_height = img.size
    rows = {}
    num_rows = 10
    row_height = img.size[1]//num_rows
    for i in range(num_rows):
        rows[i] = []

    for i in range(0, num_rows):
        for j in range(0, img_width, width):
            box = (j - padding, i*row_height - padding, j + width + padding, i*row_height + height + padding)
            a = img.crop(box)
            prediction = predict_img(a)
            rows[i].append(prediction)

    max_count = 0
    max_row = 0
    for k, v in rows.items():
        count = v.count("map")
        if count > max_count:
            max_count = count
            max_row = k

    start = 0
    end = img_width
    start_found = False
    for i in range(len(rows[max_row])-1):
        if rows[max_row][i] == "map" and rows[max_row][i+1] == "map" and not start_found:
            start = i*width
            start_found = True
            continue
        if rows[max_row][i] != "map" and rows[max_row][i+1] != "map" and start_found:
            end = i*width
            break

    return start, end


def predict_y_coord(img):
    img_width, img_height = img.size
    columns = {}
    num_columns = 12
    column_width = img_width//num_columns
    for i in range(num_columns):
        columns[i] = []

    for i in range(0, num_columns):
        for j in range(0, img_height, height):
            box = (i*column_width - padding, j - padding, i*column_width + width + padding, j + height + padding)
            a = img.crop(box)
            prediction = predict_img(a)
            columns[i].append(prediction)

    max_count = 0
    max_column = 0
    for k, v in columns.items():
        count = v.count("map")
        if count > max_count:
            max_count = count
            max_column = k

    start = 0
    end = img_height
    start_found = False
    for i in range(len(columns[max_column]) - 1):
        if columns[max_column][i] == "map" and columns[max_column][i + 1] == "map" and not start_found:
            start = i * width
            start_found = True
            continue
        if columns[max_column][i] != "map" and columns[max_column][i + 1] != "map" and start_found:
            end = i * width
            break

    return start, end


def locate_minimap(og_img):
    # The minimap will be in the bottom right of the image
    width_div = 3
    height_div = 2
    og_width, og_height = og_img.size
    og_x_start = og_width-og_width/width_div
    og_y_start = og_height-og_height/height_div
    box = (og_x_start, og_y_start, og_width, og_height)
    img = og_img.crop(box)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/bottom_right_test.png")

    x_coord = predict_x_coord(img)
    y_coord = predict_y_coord(img)
    box = (x_coord[0], y_coord[0], x_coord[1], y_coord[1])
    img = img.crop(box)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/minimap_test.png")

    return img
