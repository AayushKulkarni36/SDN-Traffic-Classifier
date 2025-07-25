import sqlite3

db_path = "/home/aayush/sdn-traffic-classifier/database/flow_logs.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS flow_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        src_ip TEXT,
        dst_ip TEXT,
        protocol INTEGER,
        src_port INTEGER,
        dst_port INTEGER,
        fwd_pkts INTEGER,
        fwd_bytes INTEGER,
        fwd_pps REAL,
        fwd_bps REAL,
        rev_pkts INTEGER,
        rev_bytes INTEGER,
        rev_pps REAL,
        rev_bps REAL,
        duration REAL,
        prediction TEXT
    )
''')

conn.commit()
conn.close()
print("Database and table created at /home/aayush/sdn-traffic-classifier/database/flow_logs.db")
