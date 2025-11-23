import httpx
import duckdb
import pandas as pd
from datetime import datetime

CONNECTION_TIMEOUT = 10.0

class CryptoIngestor:
    def __init__(self, db_con: duckdb.DuckDBPyConnection):
        self.con = db_con
        self.url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

    async def fetch_and_load(self):
        async with httpx.AsyncClient(timeout=CONNECTION_TIMEOUT) as client:
            response = await client.get(self.url)
            # raise an error if the API returns a bad status code (4xx or 5xx)
            response.raise_for_status()
            data = response.json()
        
        df = pd.DataFrame([
            {"coin": k, "price": v['usd'], "ingested_at": datetime.now()} 
            for k, v in data.items()
        ])
        
        self.con.execute("CREATE TABLE IF NOT EXISTS crypto_prices (coin VARCHAR, price DOUBLE, ingested_at TIMESTAMP)")
        self.con.execute("INSERT INTO crypto_prices SELECT * FROM df")
        return df.to_dict(orient='records')