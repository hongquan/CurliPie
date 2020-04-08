import attr
import logbook
from logbook.compat import LoggingHandler
from sanic import Sanic
from sanic import response
from sanic.response import text
from sanic_openapi import doc, swagger_blueprint
from marshmallow import Schema, ValidationError, fields
from sanic.exceptions import abort

from curlipie import curl_to_httpie


app = Sanic(__name__)
logger = logbook.Logger(__name__, logbook.DEBUG)
LoggingHandler().push_application()
app.blueprint(swagger_blueprint)


class CurlSchema(Schema):
    curl = fields.String(required=True)
    long_option = fields.Boolean(default=False)


class APIDoc:
    curl = doc.String('cURL command line')
    long_option = doc.Boolean()


app.config["API_BASEPATH"] = "/api"


@app.get("/")
@doc.exclude(True)
async def hello(request):
    return text('Sorry, doc is temporarily not available')


@app.get('/redoc')
@doc.exclude(True)
async def redoc(request):
    return response.redirect('/swagger/')


@app.post("/api/")
@doc.consumes(doc.Boolean(name='long_option'), location='body', required=False)
@doc.consumes(doc.String(name='curl'), location='body', required=True)
async def convert(request):
    schema = CurlSchema()
    try:
        args = schema.load(request.json)
    except ValidationError as e:
        return response.json(e.messages, status=400)
    try:
        result = curl_to_httpie(args['curl'], args.get('long_option'))
    except TypeError as e:
        logger.error('Got error: {}', e)
        logger.debug('Posted data: {}', args)
        raise abort(400, 'Invalid input data')
    return response.json(attr.asdict(result))
