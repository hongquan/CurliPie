import attr
from fastapi import FastAPI
from pydantic import BaseModel
from curlipie import curl_to_httpie

app = FastAPI(debug=True)


class CurlCmd(BaseModel):
    curl: str
    long_option: bool = False


@app.get("/")
def hello():
    return 'Hello'


@app.post("/api/")
def convert(cmd: CurlCmd):
    result = curl_to_httpie(cmd.curl, cmd.long_option)
    return attr.asdict(result)
