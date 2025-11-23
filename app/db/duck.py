import duckdb

# Global variable to hold the connection for simplicity in this demo.
# The database will be a file named 'crypto_data.duckdb'
DB_FILE = 'crypto_data.duckdb'
_db_connection = None

def get_db_connection():
    """Returns a singleton connection object to the DuckDB file."""
    global _db_connection
    if _db_connection is None:
        # Connects or creates the file if it doesn't exist
        _db_connection = duckdb.connect(database=DB_FILE, read_only=False)
    return _db_connection