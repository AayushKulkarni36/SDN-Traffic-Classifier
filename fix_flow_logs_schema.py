import sqlite3

db_path = "/home/aayush/sdn-traffic-classifier/database/flow_logs.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: Backup old data (only relevant columns)
cursor.execute("""
    SELECT id, timestamp, src_ip, dst_ip, protocol, src_port, dst_port,
           fwd_pkts, fwd_bytes, fwd_pps, fwd_bps,
           rev_pkts, rev_bytes, rev_pps, rev_bps,
           duration, prediction
    FROM flow_logs
""")
rows = cursor.fetchall()

# Step 2: Drop old table
cursor.execute("DROP TABLE IF EXISTS flow_logs")

# Step 3: Create clean table schema
cursor.execute("""
    CREATE TABLE flow_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        src_ip TEXT,
        dst_ip TEXT,
        protocol INTEGER,
        src_port INTEGER,
        dst_port INTEGER,
        forward_packets INTEGER,
        forward_bytes INTEGER,
        forward_pps REAL,
        forward_bps REAL,
        reverse_packets INTEGER,
        reverse_bytes INTEGER,
        reverse_pps REAL,
        reverse_bps REAL,
        duration REAL,
        prediction TEXT
    )
""")

# Step 4: Insert cleaned data back
for row in rows:
    cursor.execute("""
        INSERT INTO flow_logs (
            id, timestamp, src_ip, dst_ip, protocol, src_port, dst_port,
            forward_packets, forward_bytes, forward_pps, forward_bps,
            reverse_packets, reverse_bytes, reverse_pps, reverse_bps,
            duration, prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()

print("✅ flow_logs table cleaned and restored successfully.")
