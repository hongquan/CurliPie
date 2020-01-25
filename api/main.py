import attr
import logbook
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from curlipie import curl_to_httpie
from starlette.responses import RedirectResponse

app = FastAPI(debug=True, title='CurliPie online API')
logger = logbook.Logger(__name__, logbook.DEBUG)


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
    return attr.asdict(result)
