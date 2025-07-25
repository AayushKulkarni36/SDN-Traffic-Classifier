# SDN Traffic Classification System (Dockerized)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)

A Dockerized Software-Defined Networking (SDN) project that integrates the Ryu SDN controller, a machine learning-based traffic classification engine, and a Flask + Plotly dashboard for real-time traffic monitoring. Flow data is logged into a SQLite database and visualized through a web interface.

---

## 🧠 Features

- 🔌 **Ryu SDN Controller** with ML-based flow classification
- 📊 **Flask + Plotly Dashboard** for live monitoring
- 🗃️ **SQLite Database** to store classified flows
- 🐳 **Dockerized** for seamless deployment
- 🧪 Supports ICMP, TCP, UDP traffic simulations via Mininet

---

## 📁 Project Structure

```bash
sdn-traffic-classifier/
├── ryu_controller/
│   └── ml_controller.py         # Main Ryu app with ML integration
│
├── dashboard/
│   ├── app.py                   # Flask dashboard backend
│   └── templates/
│       ├── index.html
│       └── logs.html
│
├── database/
│   ├── flow_logs.db             # SQLite database
│   ├── schema.sql               # SQL schema for logs
│   └── init_db.py               # Initialization script
│
├── model_evaluation/
│   ├── refined_model_random_forest.joblib
│   └── refined_scaler.joblib
│
├── docker-compose.yml          # Docker Compose config
├── Dockerfile                  # Builds Ryu + ML environment
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sdn-traffic-classifier.git
cd sdn-traffic-classifier
```

### 2. Initialize the SQLite Database

```bash
docker-compose run --rm ryu python3 database/init_db.py
```

### 3. Build and Launch the Stack

```bash
docker-compose up --build
```

- The **Ryu ML Controller** will start inside a Docker container.
- The **Dashboard** will be accessible at: [http://localhost:5005](http://localhost:5005)

---

## 🧪 Test with Mininet

In a separate terminal:

```bash
sudo mn --controller=remote,ip=127.0.0.1 --topo single,3
```

Then generate traffic using:

```bash
ping, iperf, hping3, or custom scripts
```

---

## 📊 Dashboard Routes

| Route      | Description                          |
|------------|--------------------------------------|
| `/`        | Live view of recent flow logs        |
| `/logs`    | Full historical logs from SQLite     |

---

## 🐳 Optional: Manual Docker Build

```bash
docker build -t sdn-ryu .
```

---

## 🧹 Tear Down

```bash
docker-compose down
```

---

## 👤 Author

**Aayush Kulkarni**  
[LinkedIn](https://www.linkedin.com/) • [GitHub](https://github.com/your-username)

---

## 📄 License

This project is licensed under the MIT License.


## 💬 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.

---

## ⭐️ Show Your Support

If you found this project helpful, consider starring ⭐ the repository on GitHub. It motivates me to keep improving it!