import psycopg2

# Connection parameters
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'tasterealm_dev',
    'user': 'gabriel',
    'password': 'devpassword123'
}

try:
    # Connect
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    
    # Test query
    cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('staging', 'validation', 'canonical');")
    schemas = cursor.fetchall()
    
    print("✅ Connected to PostgreSQL!")
    print(f"Found schemas: {[s[0] for s in schemas]}")
    
    # Close
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
