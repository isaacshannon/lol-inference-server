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

from app import minimap, locator
from app.predicter import predict_locations
from app.user import update_user, get_user

export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_name = 'export.pkl'

path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_headers=['X-Requested-With', 'Content-Type', 'Access-Control-Allow-Origin'])
# app.mount('/static', StaticFiles(directory='app/static')) # use this for docker run
app.mount('/static', StaticFiles(directory='/home/isaac/dev/league/lol-web-server/app/static'))

@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/capture')
async def homepage(request):
    html_file = path / 'view' / 'capture.html'
    return HTMLResponse(html_file.open().read())


@app.route('/predict', methods=['POST'])
async def predict(request):
    img_data = await request.form()
    img_bytes = get_bytes(img_data)
    src_img = Image.open(io.BytesIO(img_bytes))
    # img.save("/home/isaac/dev/league/lol-web-server/app/last-img.png")

    user = get_user(img_data["user"])
    print("user: "+str(user))
    src_map, x_coord, y_coord = minimap.locate_minimap(src_img, user)
    lolmap = src_map.resize((150, 150))
    previous_positions = user["previous_positions"]
    new_positions = locator.locate_players(lolmap)
    previous_positions.append(new_positions)
    previous_positions = previous_positions[1:]
    update_user(x_coord, y_coord, previous_positions, user)
    lolmap = locator.create_composite(previous_positions, lolmap)

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
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
