import aiohttp
import asyncio
import uvicorn
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
import base64
from PIL import Image, ImageDraw

import minimap
from predicter import predict_locations

# from app import minimap
# from app.predicter import predict_locations
# from app.user import update_user, get_user

export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_name = 'export.pkl'

path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_headers=['X-Requested-With', 'Content-Type', 'Access-Control-Allow-Origin'])
app.mount('/static', StaticFiles(directory='app/static'))  # use this for docker run
app.mount('/models', StaticFiles(directory='app/models'))  # use this for docker run


# app.mount('/static', StaticFiles(directory='/home/isaac/dev/league/lol-web-server/app/static'))

@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'test.html'
    return HTMLResponse(html_file.open().read())


@app.route('/test')
async def homepage(request):
    html_file = path / 'view' / 'test.html'
    return HTMLResponse(html_file.open().read())


@app.route('/findmap', methods=['POST'])
async def findmap(request):
    img_data = await request.form()

    img_bytes = get_bytes(img_data)
    src_img = Image.open(io.BytesIO(img_bytes))
    # img.save("/home/isaac/dev/league/lol-web-server/app/last-img.png")

    src_map, x_coord, y_coord = minimap.locate_minimap(src_img)
    data = BytesIO()
    src_map.save(data, "PNG")
    data64 = base64.b64encode(data.getvalue())
    data_uri = u'data:img/png;base64,' + data64.decode('utf-8')
    return JSONResponse({
        'minimap': data_uri,
        'x0': x_coord[0],
        'x1': x_coord[1],
        'y0': y_coord[0],
        'y1': y_coord[1],
    })


@app.route('/predict', methods=['POST'])
async def predict(request):
    form = await request.form()
    img_bytes = get_bytes(form)
    src_img = Image.open(io.BytesIO(img_bytes))
    x_coord = (int(form["x0"]), int(form["x1"]))
    y_coord = (int(form["y0"]), int(form["y1"]))
    # img.save("/home/isaac/dev/league/lol-web-server/app/last-img.png")
    src_map = minimap.locate_minimap_coords(src_img, x_coord, y_coord)
    lolmap = src_map.resize((150, 150))

    pred_img = predict_locations(lolmap, src_map)
    data = BytesIO()
    pred_img.save(data, "PNG")
    data64 = base64.b64encode(data.getvalue())
    data_uri = u'data:img/png;base64,' + data64.decode('utf-8')
    return JSONResponse({'result': data_uri})


def get_bytes(form):
    img = form["imgBase64"]
    img_parts = img.split(",")
    return base64.b64decode(img_parts[1])


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8080, log_level="info")
