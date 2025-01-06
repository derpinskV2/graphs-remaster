import logging

import pandas as pd

from config.celery import app
from data.models import CSVData

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_csv_file(self, csv_file_id: int, user_id: int) -> None:
    from data.models import CSVFile

    # user = CustomUser.objects.get(id=user_id)
    csv_file = CSVFile.objects.get(id=csv_file_id)
    df = pd.read_csv(csv_file.file)
    # logger.warning(f"Processing {csv_file.file.name}")

    # Process your data here
    # For example, get the first few rows
    # preview = df.head()
    to_create = []
    for index, row in df.iterrows():  # noqa
        bg = row["CGM Glucose Value (mmol/l)"]
        serial_number = row["Serial Number"]
        ts = row["Timestamp"]
        # logger.warning(f"idx {index}: bg - {bg} serial - {serial_number} ts - {ts}")
        to_create.append(CSVData(**{"bg": bg, "serial_number": serial_number, "timestamp": ts, "user_id": user_id}))

    CSVData.objects.bulk_create(to_create)
    csv_file.processed = True
    csv_file.save()
    return None
