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
├── confusion_matrix.png
├── dashboard
│   ├── app.py
│   └── templates
├── database
│   ├── flow_logs.db
│   ├── init_db.py
│   ├── ml_controller.py
│   ├── model_evaluation
│   ├── __pycache__
│   ├── requirements.txt
│   ├── schema.sql
│   └── utils
├── datasets
│   ├── dns_training_data.csv
│   ├── game_training_data.csv
│   ├── models_all
│   ├── models_dns
│   ├── models_game
│   ├── models_ping
│   ├── models_telnet
│   ├── models_voice
│   ├── ping_training_data.csv
│   ├── telnet_training_data.csv
│   └── voice_training_data.csv
├── Dockerfile
├── feature_importances.png
├── fix_flow_logs_schema.py
├── LICENSE
├── mininet -> /usr/lib/python3/dist-packages/mininet
├── ml-venv-py39
│   ├── bin
│   ├── etc
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   ├── pyvenv.cfg
│   └── share
├── model_evaluation
│   ├── balanced_dataset.csv
│   ├── benchmark_models.py
│   ├── confusion_matrix_decision_tree.png
│   ├── confusion_matrix_knn.png
│   ├── confusion_matrix_naive_bayes.png
│   ├── confusion_matrix.png
│   ├── confusion_matrix_random_forest.png
│   └── model_comparison.csv
├── pcap
│   └── iperf3_h1_h2.json
├── README.md
├── ryu_controller
│   └── __pycache__
├── scripts
│   ├── new
│   ├── OLD
│   └── update_schema.py
├── Software-Defined-Networking.png
└── topology
    └── custom_topo.py

29 directories, 31 files

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
