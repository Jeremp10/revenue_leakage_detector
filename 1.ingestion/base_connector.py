


from email import message
import os
from datetime import datetime
import pandas as pd
import logging

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)



class BaseConnector:
    def __init__(self, config):
        self.config = config

    def connect(self):
        raise NotImplementedError("Connectors must implement this method")

    def fetch_data(self):
        raise NotImplementedError("Connectors must implement this method to fetch data from source")

    def log(self, source_name, row_count, timestamp):
        message = f"[{source_name}] Rows: {row_count}, Timestamp: {timestamp}"
        print(message)
        logging.info(message)

    def save_to_staging(self, dataframe, source_name):
        os.makedirs("staging", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"staging/{source_name}_{timestamp}.csv"
        dataframe.to_csv(filepath, index=False)
        print(f"[{source_name}] Saved {len(dataframe)} rows to {filepath}")
