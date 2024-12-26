import orjson
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from ninja_extra import NinjaExtraAPI
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


v1 = NinjaExtraAPI(
    title="Hello there.",
    version=settings.API_VERSION,
    description="I am actually going to finish this side project™",
    parser=ORJSONParser(),
    renderer=ORJSONRenderer(),
    docs_url="/docs/",
)


@v1.get("/hello")
def hello(request):
    return {"message": "Hello, World!"}
