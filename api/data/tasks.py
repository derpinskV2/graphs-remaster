import hashlib
import logging
from datetime import datetime

import pandas as pd
from celery.utils.time import make_aware, timezone
from django.core.files import File

from config.celery import app
from data.models import CSVData, CSVFile
from pathlib import Path

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_csv_file(self, user_id: int, input_dir: Path | None = None) -> None:
    input_dir = Path("data/raw")
    input_csvs = list(input_dir.glob("*.csv"))
    print(f"INPUT CSVS {input_csvs}")

    for csv_path in input_csvs:
        content = csv_path.read_bytes()  # read full file content
        hash_value = hashlib.sha256(content).hexdigest()

        with open(csv_path, "rb") as f:
            file_obj = File(f)
            csv_file, created = CSVFile.objects.update_or_create(
                user_id=user_id,
                file_hash=hash_value,
                defaults={
                    "file": file_obj,
                    "processed": False,
                },
            )
            if created:
                logger.info(f"New CSVFile created for content hash {hash_value}")
            else:
                logger.info(f"Duplicate CSV detected with hash {hash_value}; skipping or updating existing.")
    csv_files = CSVFile.objects.filter(user_id=user_id)

    for csv_file in csv_files:
        to_create = []
        print(f"Processing {csv_file}")
        for _, row in pd.read_csv(csv_file.file).iterrows():
            bg = row.get("CGM Glucose Value (mmol/l)")
            bg_input = row.get("Blood Glucose Input (mmol/l)")
            carb_input = row.get("Carbs Input (g)")
            carb_ratio = row.get("Carbs Ratio")
            total_bolus = row.get("Total Bolus (U)")
            total_insulin = row.get("Total Insulin (U)")
            total_basal = row.get("Total Basal (U)")
            insulin_delivered = row.get("Insulin Delivered (U)")
            serial_number = row.get("Serial Number")
            ts = make_aware(datetime.strptime(row.get("Timestamp"), "%Y-%m-%d %H:%M"), tz=timezone.utc)
            alarm_event = row.get("Alarm/Event")

            to_create.append(
                CSVData(
                    **{
                        "bg": bg,
                        "bg_input": bg_input,
                        "carb_input": carb_input,
                        "carb_ratio": carb_ratio,
                        "total_basal": total_basal,
                        "insulin_delivered": insulin_delivered,
                        "total_insulin": total_insulin,
                        "bolus": total_bolus,
                        "event": alarm_event,
                        "serial_number": serial_number,
                        "timestamp": ts,
                        "user_id": user_id,
                        "csv_file_id": csv_file.id,
                    }
                )
            )

        CSVData.objects.bulk_create(to_create)
        csv_file.processed = True
        csv_file.save()

    return None
