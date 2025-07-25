import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler


input_file = 'datasets/dns_training_data.csv'
output_folder = 'models_dns'
traffic_label = 'dns'
feature_list_path = 'scripts/feature_list.csv'

os.makedirs(output_folder, exist_ok=True)

print(f"Loading {input_file}...")
df = pd.read_csv(input_file)

print(f"Assigning label '{traffic_label}'...")
df['Traffic Type'] = traffic_label

print("Filling missing values...")
df.fillna(df.mean(numeric_only=True), inplace=True)


X = df.drop(columns=['Traffic Type'])
y = df['Traffic Type']


joblib.dump(X, os.path.join(output_folder, 'features_raw.joblib'))


X = pd.get_dummies(X)
if os.path.exists(feature_list_path):
    feature_list = pd.read_csv(feature_list_path, header=None)[0].tolist()
    X = X.reindex(columns=feature_list, fill_value=0)
else:
    raise FileNotFoundError("scripts/feature_list.csv not found. Run extract_feature_union.py first.")


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


joblib.dump(X_scaled, os.path.join(output_folder, 'features_scaled.joblib'))
joblib.dump(y, os.path.join(output_folder, 'labels_raw.joblib'))

print(f"Saved to {output_folder}/: features_raw.joblib, features_scaled.joblib, labels_raw.joblib")
