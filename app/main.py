from fastapi import FastAPI, BackgroundTasks
from app.services.ingestor import CryptoIngestor
from app.db.duck import get_db_connection

app = FastAPI(title="CryptoLake Senior Demo")

@app.on_event("startup")
def startup():
    # Initialize DB table on boot
    con = get_db_connection()
    con.execute("CREATE TABLE IF NOT EXISTS crypto_prices (coin VARCHAR, price DOUBLE, ingested_at TIMESTAMP)")

@app.get("/ingest")
async def trigger_etl(background_tasks: BackgroundTasks):
    """Triggers the ETL job asynchronously."""
    ingestor = CryptoIngestor(get_db_connection())
    # In a real scenario, this would be a cron job or Airflow task
    data = await ingestor.fetch_and_load()
    return {"status": "Ingested", "rows": len(data)}

@app.get("/analytics/avg-price")
def get_analytics():
    """Demonstrates OLAP capabilities of DuckDB."""
    con = get_db_connection()
    # Complex aggregation made easy by DuckDB
    result = con.execute("SELECT coin, AVG(price) as avg_price FROM crypto_prices GROUP BY coin").fetchall()
    return {"analytics": result}