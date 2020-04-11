import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
import base64
from PIL import Image, ImageEnhance
import sys
import time

import minimap
from predicter import predict_locations
import logging
import sentry_sdk
from sentry_sdk import capture_exception

sentry_sdk.init("https://0e27027a292a41d3a334a9d5c4fde2fa@o370311.ingest.sentry.io/5196683")

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_headers=['X-Requested-With', 'Content-Type', 'Access-Control-Allow-Origin'])
app.mount('/static', StaticFiles(directory='app/static'))
app.mount('/models', StaticFiles(directory='app/models'))

logs = logging.getLogger("request data")


@app.route('/predict', methods=['POST'])
async def predict(request):
    form = await request.form()
    img_bytes = get_bytes(form)
    src_img = Image.open(BytesIO(img_bytes)).convert('RGBA')
    src_map = minimap.locate_minimap(src_img)
    lolmap = src_map.resize((150, 150), Image.BICUBIC)
    converter = ImageEnhance.Color(lolmap)
    lolmap = converter.enhance(3)

    start_time = time.time()
    preds = predict_locations(lolmap)
    elapsed_time = time.time() - start_time

    logs.info(f"Prediction time: {elapsed_time}")

    return JSONResponse({'predictions': preds})


def get_bytes(form):
    img = form["imgBase64"]
    img_parts = img.split(",")
    return base64.b64decode(img_parts[1])


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8080, log_level="info")
