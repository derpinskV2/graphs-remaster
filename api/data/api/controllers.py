import logging

from django.shortcuts import aget_object_or_404, get_object_or_404
from ninja import Form
from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_delete, paginate
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.schemas import PaginatedResponseSchema
from ninja_jwt.authentication import JWTAuth

from data.models import CSVFile, CSVData
from data.api.schemas import CSVFileSchema, CSVDataSchema
from data.tasks import process_csv_file


logger = logging.getLogger(__name__)


@api_controller("/csv-files", tags=["CSV Files"], auth=JWTAuth())
class CSVFileController(ControllerBase):

    @http_get(response=list[CSVFileSchema])
    async def list_csv_files(self, request):
        return [csv async for csv in CSVFile.objects.all()]

    @http_get("/{id}", response=CSVFileSchema)
    async def get_csv_file(self, request, id: int):
        return await aget_object_or_404(CSVFile, id=id)

    @http_post(response=CSVFileSchema)
    async def create_csv_file(self, request, data: Form[CSVFileSchema]):
        return await CSVFile.objects.acreate(file=request.FILES["file"])

    @http_post("/{id}/process")
    def queue_csv_file(self, request, id: int):
        csv_file = get_object_or_404(CSVFile, id=id)
        # process_csv_file.apply_async(
        #     args=(
        #         csv_file.id,
        #         request.user.id,
        #     )
        # )
        process_csv_file.delay(csv_file.id, request.user.id)
        return {"message": f"CSV file {id} queued."}

    @http_delete("/{id}")
    async def delete_csv_file(self, request, id: int):
        csv_file = await aget_object_or_404(CSVFile, id=id)

        await csv_file.adelete()
        return {"message": f"CSV file {id} deleted"}


@api_controller("/csv-data", tags=["CSV Data"])
class CSVDataController(ControllerBase):

    @http_get(response=PaginatedResponseSchema[CSVDataSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    async def list_csv_data(self, request):
        return [csv async for csv in CSVData.objects.all()]

    @http_get("/{id}", response=CSVDataSchema)
    async def get_csv_file(self, request, id: int):
        return await aget_object_or_404(CSVData, id=id)

    @http_delete("/{id}")
    async def delete_csv_file(self, request, id: int):
        csv_file = await aget_object_or_404(CSVFile, id=id)
        await csv_file.adelete()
        return {"message": f"CSV data {id} deleted"}
