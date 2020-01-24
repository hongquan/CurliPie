import attr
from fastapi import FastAPI
from pydantic import BaseModel
from curlipie import curl_to_httpie
from starlette.responses import RedirectResponse

app = FastAPI(debug=True, title='CurliPie online API')


class CurlCmd(BaseModel):
    curl: str
    long_option: bool = False


@app.get("/")
def hello():
    return RedirectResponse('/redoc')


@app.post("/api/")
def convert(cmd: CurlCmd):
    result = curl_to_httpie(cmd.curl, cmd.long_option)
    return attr.asdict(result)
