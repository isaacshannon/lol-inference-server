import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
import base64
import cv2
from PIL import Image, ImageDraw
import os

from app import minimap

export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_name = 'export.pkl'

# classes = ['black', 'grizzly', 'teddys']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type', 'Access-Control-Allow-Origin'])
# app.mount('/static', StaticFiles(directory='app/static')) # use this for docker run
app.mount('/static', StaticFiles(directory='/home/isaac/dev/league/lol-web-server/app/static'))


def draw_grid(draw, labels):
    grid_size = 10
    # for x in range(grid_lines):
    #     z = grid_size*x
    #     draw.line([z, 0, z, 150], fill=fill)
    #     draw.line([0, z, 150, z], fill=fill)

    fill = (0, 255, 255, 96)
    for l in labels:
        x = l[0] * grid_size
        y = l[1] * grid_size
        draw.rectangle((x, y, x + grid_size, y + grid_size), fill=fill)


# async def download_file(url, dest):
#     if dest.exists(): return
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.read()
#             with open(dest, 'wb') as f:
#                 f.write(data)


async def setup_learner():
    # await download_file(export_file_url, path / export_file_name)
    try:
        # learn = load_learner("./app/models", "predict-2019-12-28.pth") Use this for docker run
        learn = load_learner("/home/isaac/dev/league/lol-web-server/app/models", "predict.pth")
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})


@app.route('/capture')
async def homepage(request):
    html_file = path / 'view' / 'capture.html'
    return HTMLResponse(html_file.open().read())


@app.route('/predict', methods=['POST'])
async def predict(request):
    img_data = await request.form()
    img_bytes = get_bytes(img_data)
    img = Image.open(io.BytesIO(img_bytes))

    lolmap = minimap.locate_minimap(img)
    lolmap = lolmap.resize((150,150))

    imgByteArr = BytesIO()
    lolmap.save(imgByteArr, format='PNG')
    fai_img = open_image(imgByteArr)
    prediction = str(learn.predict(fai_img)[0])
    print(prediction)
    labels = [(int(s.split("-")[0]), int(s.split("-")[1])) for s in prediction.split(";")]

    overlay = Image.new('RGBA', lolmap.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw_grid(draw, labels)
    out = Image.alpha_composite(lolmap, overlay)
    data = BytesIO()
    out.save(data, "PNG")
    data64 = base64.b64encode(data.getvalue())
    data_uri = u'data:img/png;base64,' + data64.decode('utf-8')

    return JSONResponse({'result': data_uri})


def get_bytes(form):
    img = form["imgBase64"]
    img_parts = img.split(",")
    return base64.b64decode(img_parts[1])


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
