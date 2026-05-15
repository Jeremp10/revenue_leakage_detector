import pandas as pd
from .base_connector import BaseConnector
import os
from datetime import datetime

class CSVConnector(BaseConnector):
    def connect(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        return file_path

    def extract(self, file_path, source_name):
        file_path = self.connect(file_path)
        dataframe = pd.read_csv(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log(source_name, len(dataframe), timestamp)
        self.save_to_staging(dataframe, source_name)
        return dataframe
