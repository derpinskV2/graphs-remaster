import logging
from django.shortcuts import aget_object_or_404, get_object_or_404
from ninja import Form
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, http_get, http_delete, paginate, http_post
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.permissions import IsAuthenticated
from ninja_extra.schemas import PaginatedResponseSchema
from ninja_jwt.authentication import JWTAuth
from data.models import CSVFile, CSVData
from data.api.schemas import CSVFileSchema, CSVDataSchema
from core.permissions import S3PresignedURLMixin
from data.tasks import process_csv_file

logger = logging.getLogger(__name__)


@api_controller("/csv-files", tags=["CSV Files"], auth=None, permissions=[IsAuthenticated])
class CSVFileController(ControllerBase, S3PresignedURLMixin):

    @http_get(response=PaginatedResponseSchema[CSVFileSchema])
    @paginate(PageNumberPaginationExtra, page_size=50)
    async def list_csv_files(self, request):
        return [csv async for csv in CSVFile.objects.filter(user=request.user)]

    @http_get(path="/{file_id}", response=CSVFileSchema, auth=JWTAuth())
    def get_file(self, request, file_id: int):
        csv_file = get_object_or_404(CSVFile, id=file_id)
        try:
            url = self.get_presigned_url_for_file(csv_file, request.user)
        except PermissionError:
            raise HttpError(403, "You are not allowed to access this file.")

        schema_obj = CSVFileSchema.model_validate(csv_file)
        schema_obj.presigned_url = url
        return schema_obj

    @http_post(response=CSVFileSchema)
    async def create_csv_file(self, request, data: Form[CSVFileSchema]):
        return await CSVFile.objects.acreate(file=request.FILES["file"])

    @http_post("/process/all")
    def queue_csv_files(self, request):
        process_csv_file.delay(request.user.id)
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
