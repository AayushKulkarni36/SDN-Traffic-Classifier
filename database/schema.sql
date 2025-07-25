CREATE TABLE IF NOT EXISTS flow_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    src_ip TEXT NOT NULL,
    dst_ip TEXT NOT NULL,
    protocol INTEGER,
    forward_packets INTEGER,
    forward_bytes INTEGER,
    fwd_pps REAL,
    fwd_bps REAL,
    reverse_packets INTEGER,
    reverse_bytes INTEGER,
    rev_pps REAL,
    rev_bps REAL,
    duration REAL,
    prediction TEXT
);
