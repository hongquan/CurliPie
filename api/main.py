from pathlib import Path

import logbook
from logbook.compat import LoggingHandler
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from curlipie import curl_to_httpie
from starlette.responses import RedirectResponse


PUBLIC_DIR = Path(__file__).parent / 'public'
app = FastAPI(debug=True, title='CurliPie online API')
logger = logbook.Logger(__name__, logbook.DEBUG)
LoggingHandler().push_application()


class CurlCmd(BaseModel):
    curl: str
    long_option: bool = False


@app.get("/")
async def hello():
    return RedirectResponse('/redoc')


@app.post("/api/")
async def convert(cmd: CurlCmd):
    try:
        result = curl_to_httpie(cmd.curl, cmd.long_option)
    except TypeError as e:
        logger.error('Got error: {}', e)
        logger.debug('Posted data: {}', cmd)
        raise HTTPException(400, 'Invalid input data')
    return result


app.mount('/demo/', StaticFiles(directory=PUBLIC_DIR, html=True))
