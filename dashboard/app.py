from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_PATH = "/home/aayush/sdn-traffic-classifier/database/flow_logs.db"

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, src_ip, dst_ip, protocol, src_port, dst_port,
               fwd_pkts, fwd_bytes, rev_pkts, rev_bytes, duration, prediction
        FROM flow_logs ORDER BY id DESC LIMIT 500
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def dashboard():
    data = fetch_data()
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True,port=5050)
