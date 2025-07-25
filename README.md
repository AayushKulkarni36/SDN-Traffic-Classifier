# 🧠 SDN Traffic Classifier

A machine learning-based traffic classification system for **Software-Defined Networking (SDN)** using **Ryu**, **Mininet**, and **Flask**. The system classifies network flows in real-time using a trained Random Forest model and logs results into a SQLite database, which are visualized via an interactive dashboard.

---

## 🚀 Features

- ✅ Real-time traffic classification in SDN using Ryu controller
- ✅ Supports flow feature extraction: packets, bytes, duration, protocol (both directions)
- ✅ ML-based classification using Random Forest
- ✅ Traffic logging into a local SQLite database
- ✅ Flask + Plotly dashboard for real-time flow visualization
- ✅ Blocks malicious traffic (`malware`, `botnet`, `telnet`, etc.) using flow rules
- ✅ Docker-ready architecture (coming soon)

---

## 📁 Project Structure

```
sdn-traffic-classifier/
├── ryu_controller/           # Ryu controller with ML classification
│   └── ml_controller.py
│
├── scripts/new/              # Dataset + traffic generation
│   ├── generate_mixed_traffic.py
│   └── refined_traffic_dataset.csv
│
├── model_evaluation/         # Trained Random Forest model + scaler
│   ├── refined_model_random_forest.joblib
│   ├── refined_scaler.joblib
│   └── feature_list_refined.csv
│
├── dashboard/                # Flask + Plotly web dashboard
│   ├── app.py
│   └── templates/index.html
│
├── database/                 # SQLite DB (created at runtime)
│   └── flow_logs.db
│
├── Dockerfile                # Docker setup (TBD)
├── requirements.txt          # Python dependencies
├── .gitignore
├── LICENSE                   # MIT License
└── README.md
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AayushKulkarni36/SDN-Traffic-Classifier.git
cd SDN-Traffic-Classifier
```

### 2. Create Virtual Environment (optional but recommended)

```bash
python3 -m venv ml-venv-py39
source ml-venv-py39/bin/activate
pip install -r requirements.txt
```

---

## 🧠 ML Model Information

- 📊 **Model:** Random Forest Classifier (trained on 16 flow-level features)
- 🗂️ **Features:** Packet Count, Byte Count, Duration, Protocol (both directions), PPS, BPS, etc.
- 🧪 **Dataset:** `refined_traffic_dataset.csv`
- 🧠 **Trained model:** `refined_model_random_forest.joblib`

---

## ⚙️ How to Use

### 1. Start the Ryu Controller

```bash
ryu-manager ryu_controller/ml_controller.py
```

### 2. Start Mininet with Custom Topology

```bash
sudo mn --custom topology/custom_topo.py --topo mytopo --controller=remote
```

### 3. Generate Traffic

```bash
python3 scripts/new/generate_mixed_traffic.py
```

### 4. Launch the Flask Dashboard

```bash
cd dashboard
python3 app.py
```

Access it at: [http://localhost:5000](http://localhost:5000)

---

## 📊 Dashboard Preview

- View real-time classified flows
- Visualize classes: Normal, Botnet, Malware, Telnet, etc.
- Includes timestamps, flow keys, and protocol details

---

## 🐳 Docker (coming soon)

We'll soon include:
- `Dockerfile` for Ryu controller
- `docker-compose` for dashboard + controller
- Lightweight build for development or deployment

---

## 🪪 License

This project is licensed under the MIT License.  
See [`LICENSE`](LICENSE) file for details.

---

## 🙋 Author

- **Aayush Kulkarni**
- GitHub: [@AayushKulkarni36](https://github.com/AayushKulkarni36)

---

## 💬 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.

---

## ⭐️ Show Your Support

If you found this project helpful, consider starring ⭐ the repository on GitHub. It motivates me to keep improving it!
