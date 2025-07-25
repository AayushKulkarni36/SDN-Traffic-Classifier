import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

model_folders = ['models_dns', 'models_game', 'models_ping', 'models_telnet', 'models_voice']
feature_list_path = 'scripts/feature_list.csv'
output_path = 'models_all/scaler.joblib'


if not os.path.exists(feature_list_path):
    raise FileNotFoundError("Feature list not found. Run extract_feature.py first.")
feature_list = pd.read_csv(feature_list_path, header=None)[0].tolist()

X_all = []

print("Collecting raw features from each traffic type...")

for folder in model_folders:
    path = os.path.join(folder, 'features_raw.joblib')
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing raw feature file: {path}")
    
    df = joblib.load(path)
    df = pd.get_dummies(df)
    df = df.reindex(columns=feature_list, fill_value=0)
    X_all.append(df)


X_combined = pd.concat(X_all, ignore_index=True)

print(" Fitting StandardScaler on combined dataset...")
scaler = StandardScaler()
scaler.fit(X_combined)

os.makedirs('models_all', exist_ok=True)
joblib.dump(scaler, output_path)

print(f"Saved combined scaler to {output_path}")
