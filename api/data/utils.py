import logging

import pandas as pd

from data.models import CSVData

logger = logging.getLogger(__name__)


def process_csv(csv_file):
    # open csv file using pandas and add to database data
    df = pd.read_csv(csv_file)

    # Process your data here
    # For example, get the first few rows
    # preview = df.head()
    to_create = []
    for index, row in df.iterrows():
        bg = row["CGM Glucose Value (mmol/l)"]
        serial_number = row["Serial Number"]
        ts = row["Timestamp"]
        logger.warning(f"idx {index}: bg - {bg} serial - {serial_number} ts - {ts}")
        to_create.append(CSVData(**{"bg": bg, "serial_number": serial_number, "timestamp": ts}))

    CSVData.objects.bulk_create(to_create)

    # logger.warning(preview)
