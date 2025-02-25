from http import HTTPStatus
from pathlib import Path

import logbook
from logbook.compat import LoggingHandler
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from pydantic.config import JsonValue
from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from curlipie import curl_to_httpie
from curlipie.pie import ConversionResult


PUBLIC_DIR = Path(__file__).parent / '_public'
TEMPLATE_DIR = Path(__file__).parent / 'templates'
LoggingHandler().push_application()


class Settings(BaseSettings):
    tracking: bool = False


EXAMPLE: JsonValue = {
    'curl': 'curl -X POST http://quan.hoabinh.vn/api/users --user admin:xxx -d name=meow',
    'long_option': False,
}


class CurlCmd(BaseModel):
    model_config = ConfigDict(json_schema_extra={'example': EXAMPLE})
    curl: str
    long_option: bool = False


app = FastAPI(debug=True, title='CurliPie online API')
logger = logbook.Logger(__name__, logbook.DEBUG)
templates = Jinja2Templates(directory=TEMPLATE_DIR)
settings = Settings()


@app.get('/', response_class=HTMLResponse)
def hello(request: Request):
    return templates.TemplateResponse('index.jinja', {'request': request, 'TRACKING': settings.tracking})


@app.post('/api/', response_model=ConversionResult)
async def convert(cmd: CurlCmd):
    try:
        result = curl_to_httpie(cmd.curl, cmd.long_option)
    except TypeError as e:
        logger.error('Got error: {}', e)
        logger.debug('Posted data: {}', cmd)
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Invalid input data')
    return result


app.mount('/static', StaticFiles(directory=PUBLIC_DIR, html=True), name='static')
