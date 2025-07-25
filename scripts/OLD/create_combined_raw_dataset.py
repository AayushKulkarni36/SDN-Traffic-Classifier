import pandas as pd
import os
import joblib

dataset_paths = {
    'dns': 'datasets/dns_training_data.csv',
    'game': 'datasets/game_training_data.csv',
    'ping': 'datasets/ping_training_data.csv',
    'telnet': 'datasets/telnet_training_data.csv',
    'voice': 'datasets/voice_training_data.csv'
}

df_list = []

for label, path in dataset_paths.items():
    df = pd.read_csv(path)
    df['Traffic Type'] = label
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv('combined.csv', index=False)

y = combined_df['Traffic Type']
X = combined_df.drop(columns=['Traffic Type'])

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)
os.makedirs('models_all', exist_ok=True)
joblib.dump(X, 'models_all/features_raw.joblib')               
joblib.dump(y_encoded, 'models_all/labels_encoded.joblib')    
joblib.dump(le.classes_, 'models_all/label_classes.joblib')    

print(" Saved combined.csv, features_raw.joblib, labels_encoded.joblib, label_classes.joblib")
