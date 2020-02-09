from fastai.vision import *
from io import BytesIO

learn = load_learner("./app/models", "minimap.pth")
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


def predict_img(img):
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='PNG')
    fai_img = open_image(imgByteArr)
    prediction = learn.predict(fai_img)[0]
    return str(prediction)


def predict_x_coord(img):
    num_rows = 10
    row_height = img.size[1] // num_rows

    row_count = None  # A running count of which row column has a "map" value.
    map_rows = 0  # A count of rows which likely contain a map.
    for i in range(num_rows - 1, 0, -2):
        predictions, is_map = get_row_predictions(i * row_height, img)
        print(predictions)
        # ignore this row, it doesn't contain a map
        if not is_map:
            continue

        map_rows += 1
        if row_count is None:
            row_count = predictions
        else:
            row_count = [predictions[i] + row_count[i] for i in range(len(row_count))]

        # To avoid running expensive predictions, we only want 2 rows which likely contain maps.
        if map_rows >= 2:
            break
    print(row_count)
    return get_start_end(row_count, width, img.size[0])


def get_row_predictions(y, img):
    img_width, img_height = img.size
    predictions = []
    for j in range(0, img_width, width):
        box = (j - padding, y - padding, j + width + padding, y + height + padding)
        a = img.crop(box)
        prediction = predict_img(a)
        predictions.append(prediction)
    pred_map = {
        "map": 1,
        "nomap": 0,
    }
    predictions = [pred_map[p] for p in predictions]
    return predictions, predictions.count(1) > 12


def predict_y_coord(img):
    num_columns = 12
    column_width = img.size[0] // num_columns

    column_count = None  # A running count of which column row has a "map" value.
    map_columns = 0  # A count of rows which likely contain a map.
    for i in range(num_columns - 1, 0, -2):
        predictions, is_map = get_column_predictions(i * column_width, img)
        # ignore this row, it doesn't contain a map
        if not is_map:
            continue

        map_columns += 1
        if column_count is None:
            column_count = predictions
        else:
            column_count = [predictions[i] + column_count[i] for i in range(len(column_count))]

        # To avoid running expensive predictions, we only want 2 columns which likely contain maps.
        if map_columns >= 2:
            break
    return get_start_end(column_count, height, img.size[1])


def get_column_predictions(x, img):
    img_width, img_height = img.size
    predictions = []
    for j in range(0, img_height, height):
        box = (x - padding, j, x + width + padding, j + height + 2*padding)
        a = img.crop(box)
        prediction = predict_img(a)
        predictions.append(prediction)
    pred_map = {
        "map": 1,
        "nomap": 0,
    }
    predictions = [pred_map[p] for p in predictions]
    return predictions, predictions.count(1) > 5


def get_start_end(counts, inc, max_val):
    start = 0
    end = 0
    window_size = len(counts) // 15
    for i in range(len(counts) - window_size // 2):
        window = counts[i:i + window_size]
        window_sum = sum(window)
        if window_sum > window_size and not start:
            start = i * inc
        window = counts[i:i + window_size * 2]
        window_sum = sum(window)
        if window_sum < 2 and start:
            end = i * inc
            break
    #  The map extends to the edge of the screen
    if not end or end > max_val:
        end = max_val
    return start, end


def get_bottom_corner(og_img):
    # The minimap will be in the bottom right of the image
    width_div = 3
    height_div = 2
    og_width, og_height = og_img.size
    og_x_start = og_width - og_width / width_div
    og_y_start = og_height - og_height / height_div
    box = (og_x_start, og_y_start, og_width, og_height)
    return og_img.crop(box)


def locate_minimap(og_img):
    img = get_bottom_corner(og_img)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/last_bottom_right.png")

    # Attempt to retrieve the x,y coordinates from the user record
    x_coord = predict_x_coord(img)
    y_coord = predict_y_coord(img)
    delta_x = x_coord[1] - x_coord[0]
    delta_y = y_coord[1] - y_coord[0]
    delta = min(delta_x, delta_y)
    x_coord = (x_coord[1]-delta, x_coord[1])
    y_coord = (y_coord[1]-delta, y_coord[1])

    box = (x_coord[0], y_coord[0], x_coord[1], y_coord[1])
    img = img.crop(box)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/last_mini_map.png")
    return img, x_coord, y_coord


def locate_minimap_coords(og_img, x_coord, y_coord):
    img = get_bottom_corner(og_img)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/last_bottom_right.png")

    box = (x_coord[0], y_coord[0], x_coord[1], y_coord[1])
    img = img.crop(box)
    # img.save("/home/isaac/dev/league/lol-web-server/app/test/last_mini_map.png")
    return img
