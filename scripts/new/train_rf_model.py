import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from joblib import dump
from imblearn.over_sampling import SMOTE
import os
import seaborn as sns
import matplotlib.pyplot as plt


data_path = '/home/aayush/sdn-traffic-classifier/scripts/new/balanced_dataset.csv' 
df = pd.read_csv(data_path)
X = df.drop('Label', axis=1)
y = df['Label']

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42, stratify=y
)
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)


feature_list = list(X.columns)
feature_list_path = '/home/aayush/sdn-traffic-classifier/model_evaluation/feature_list_refined.csv'
with open(feature_list_path, 'w') as f:
    for feat in feature_list:
        f.write(f"{feat}\n")


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)


model = RandomForestClassifier(n_estimators=200, max_depth=20, class_weight='balanced')
model.fit(X_train_scaled, y_train_res)
y_pred = model.predict(X_test_scaled)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"\n Accuracy: {acc:.4f}")
print(f" Precision (weighted): {prec:.4f}")
print(f"Recall (weighted): {rec:.4f}")
print(f" F1-Score (weighted): {f1:.4f}")


cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

model_path = '/home/aayush/sdn-traffic-classifier/model_evaluation/refined_model_random_forest.joblib'
scaler_path = '/home/aayush/sdn-traffic-classifier/model_evaluation/refined_scaler.joblib'

dump(model, model_path)
dump(scaler, scaler_path)


print("Trained Classes:", model.classes_)

print("\nModel and scaler saved successfully.")

import pandas as pd
data_path = '/home/aayush/sdn-traffic-classifier/scripts/new/balanced_dataset.csv' 
df = pd.read_csv(data_path)
print(df['Label'].value_counts())

importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': feature_list,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nTop 15 Important Features:")
print(feature_importance_df.head(15))


