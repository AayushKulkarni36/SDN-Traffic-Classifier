import joblib
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

model_folders = ['models_dns', 'models_game', 'models_ping', 'models_telnet', 'models_voice']

X_list = []
label_text_list = []

print("Merging preprocessed datasets...")

for folder in model_folders:
    print(f"Loading from {folder}...")
    X = joblib.load(os.path.join(folder, 'features_scaled.joblib')) #os.path.join() is used to load a file using its path eg= folder/filename
    y_raw = joblib.load(os.path.join(folder, 'labels_raw.joblib'))

    X_list.append(X)
    label_text_list.extend(y_raw)

# Encode all labels with a consistent encoder
encoder = LabelEncoder()
y_combined_encoded = encoder.fit_transform(label_text_list)

# Stack features
X_combined = np.vstack(X_list)

# Save merged dataset and label classes
output_folder = 'models_all'
os.makedirs(output_folder, exist_ok=True)

joblib.dump(X_combined, os.path.join(output_folder, 'features_scaled.joblib'))
joblib.dump(y_combined_encoded, os.path.join(output_folder, 'labels_encoded.joblib'))
joblib.dump(encoder.classes_, os.path.join(output_folder, 'label_classes.joblib'))

print(f"Merged dataset and label classes saved to {output_folder}/")
