from PIL import ImageEnhance


def enhance_img(img):
    img = img.resize((150,150))
    # converter = ImageEnhance.Color(img)
    # img = converter.enhance(1.5)
    return img
