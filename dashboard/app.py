from flask import Flask, render_template
import sqlite3
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
db_path = 'database/flow_logs.db'

@app.route('/')
def dashboard():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT timestamp, src_ip, dst_ip, protocol, src_port, dst_port, fwd_pkts, fwd_bytes, rev_pkts, rev_bytes, duration, prediction FROM flow_logs ORDER BY timestamp DESC LIMIT 100")
    rows = c.fetchall()
    rows = [
    (utc_to_ist(row[0]), *row[1:])  # Convert timestamp column to IST
    for row in rows
]
    conn.close()
    return render_template('index.html', data=rows)

@app.route('/logs')
def full_logs():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM flow_logs ORDER BY timestamp DESC")
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return render_template('logs.html', rows=rows, columns=columns)

def utc_to_ist(utc_str):
    utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
    ist_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30)))
    return ist_dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True,port=5004)
