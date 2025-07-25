import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

print("Loading combined.csv ...")
df = pd.read_csv('combined.csv')

X = df.drop(columns=['Traffic Type'])
y = df['Traffic Type']

print("Encoding labels ...")
le = LabelEncoder()
y_encoded = le.fit_transform(y)


os.makedirs('models_all', exist_ok=True)
joblib.dump(X, 'models_all/features_raw.joblib')
joblib.dump(y_encoded, 'models_all/labels_encoded.joblib')
joblib.dump(le.classes_, 'models_all/label_classes.joblib')

print("Saved features_raw.joblib, labels_encoded.joblib, and label_classes.joblib to models_all/")
