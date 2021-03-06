import os
import sys
from api_data.process import DataProcessor, DataIngestor
from api_data.fetch import Fetch
import asyncio
import pandas as pd
from dark_sky_app import settings
import psycopg2
from sqlalchemy import create_engine

class MasterCrawler(object):
    
    def __init__(self, key, mapping_data):
        self.mapping_data = mapping_data
        self.key = key
    
    def crawl(self):
        fetch = Fetch(self.mapping_data)
        # calling main
        response_data = asyncio.run(fetch.main(
                url_template=fetch.template, 
                secret_key=self.key, 
                loc_data=self.mapping_data, 
                exclude_args = fetch.exclude_args))
        processor = DataProcessor(response_data)
        processed_data = processor.process()
        
        ingestor = DataIngestor()
        
        for key, value in processed_data.items():
            if not value.empty:
                value.to_csv(f"{key}.csv", index=False)
                ingestor.ingest(df=value, table_name=key)
        
        ingestor.dispose_and_close()

class DBConnector(object):
    
    def __init__(self, key):
        user = settings.db_from_env['USER']
        password = settings.db_from_env['PASSWORD']
        database_name = settings.db_from_env['NAME']
        host = settings.db_from_env['HOST']
        port = settings.db_from_env['PORT']
        database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}'
        self.conn = psycopg2.connect(dbname=database_name, user=user, host=host, password=password, port=port)
        self.engine = create_engine(database_url, echo=True)
        self.cursor = self.conn.cursor()
        
    def grab_mapping_data(self):
        self.cursor.execute('SELECT latitude, longitude FROM api_data_mappingdata')
        data = list(self.cursor.fetchall())
        return data
