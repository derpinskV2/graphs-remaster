import orjson
import logging
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from ninja_extra import NinjaExtraAPI
from django.conf import settings
from ninja_jwt.controller import NinjaJWTDefaultController
from .celery import debug_task

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


v1.register_controllers("data.api.controllers.CSVFileController")
v1.register_controllers("data.api.controllers.CSVDataController")
v1.register_controllers(NinjaJWTDefaultController)


@v1.get("/debug-celery")
def health(request):
    try:
        debug_task.delay()
    except Exception as e:
        logger.exception(e)

    return {"Hello": "123"}
