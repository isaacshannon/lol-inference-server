import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
import base64
from PIL import Image
import sys

import minimap
from predicter import predict_locations

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_headers=['X-Requested-With', 'Content-Type', 'Access-Control-Allow-Origin'])
app.mount('/static', StaticFiles(directory='app/static'))
app.mount('/models', StaticFiles(directory='app/models'))


@app.route('/findmap', methods=['POST'])
async def findmap(request):
    img_data = await request.form()

    img_bytes = get_bytes(img_data)
    src_img = Image.open(BytesIO(img_bytes))
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
    src_img = Image.open(BytesIO(img_bytes))
    src_map = minimap.locate_minimap(src_img)
    lolmap = src_map.resize((150, 150), Image.BICUBIC)

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
