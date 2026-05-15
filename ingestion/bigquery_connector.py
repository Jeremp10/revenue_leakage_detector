import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
from .base_connector import BaseConnector

class BigQueryConnector(BaseConnector):
    def connect(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.config["credentials_path"],
            scopes=["https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform"]
        )
        self.client = bigquery.Client(
            credentials=credentials,
            project=self.config["project_id"]
        )

    def extract(self, date_from, date_to):
        self.connect()
        query = f"""
        SELECT
          oi.order_id,
          oi.user_id,
          oi.product_id,
          oi.status,
          oi.created_at,
          oi.shipped_at,
          oi.delivered_at,
          oi.returned_at,
          oi.sale_price,
          ii.cost
        FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
        LEFT JOIN `bigquery-public-data.thelook_ecommerce.inventory_items` ii
            ON oi.inventory_item_id = ii.id
        WHERE oi.created_at BETWEEN '{date_from}' AND '{date_to}'
            """
        #run query
        dataframe = self.client.query(query).to_dataframe()


        #using base connector methods to log and save data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log("bigquery_thelook", len(dataframe), timestamp)
        self.save_to_staging(dataframe, "thelook")

        return dataframe
