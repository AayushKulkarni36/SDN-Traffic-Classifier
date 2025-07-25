import sqlite3

db_path = "/home/aayush/sdn-traffic-classifier/database/flow_logs.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add new columns if they don't exist
try:
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN forward_packets INTEGER")
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN forward_bytes INTEGER")
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN reverse_packets INTEGER")
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN reverse_bytes INTEGER")
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN duration REAL")
    cursor.execute("ALTER TABLE flow_logs ADD COLUMN prediction TEXT")
except sqlite3.OperationalError as e:
    print("Column might already exist or error occurred:", e)

conn.commit()
conn.close()
print("Schema update complete.")
