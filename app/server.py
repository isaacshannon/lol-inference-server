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

@app.route('/predict', methods=['POST'])
async def predict(request):
    form = await request.form()
    img_bytes = get_bytes(form)
    src_img = Image.open(BytesIO(img_bytes))
    src_map = minimap.locate_minimap(src_img)
    lolmap = src_map.resize((150, 150), Image.BICUBIC)

    preds = predict_locations(lolmap)
    return JSONResponse({'predictions': preds})


def get_bytes(form):
    img = form["imgBase64"]
    img_parts = img.split(",")
    return base64.b64decode(img_parts[1])


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8080, log_level="info")
