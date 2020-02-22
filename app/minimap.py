def locate_minimap(img):
    width, height = img.size
    dy = (height - width) / 2
    img = img.crop((0, dy, width, dy + width))
    return img

