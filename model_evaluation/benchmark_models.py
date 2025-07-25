import os 
import joblib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

DATA_DIR = 'models_all'

print("Loading combined preprocessed dataset...")

X = joblib.load(os.path.join(DATA_DIR, 'features_scaled.joblib'))
y = joblib.load(os.path.join(DATA_DIR, 'labels_encoded.joblib'))
class_names = joblib.load(os.path.join(DATA_DIR, 'label_classes.joblib'))  


os.makedirs('model_evaluation', exist_ok=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier()
}

results = []

print("Evaluating models...")

for name, model in models.items():
    print(f"🔧 Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    results.append({
        'Model': name,
        'Accuracy': acc,    
        'Precision': prec,
        'Recall': rec,
        'F1 Score': f1
    })

    model_path = f'model_evaluation/model_{name.replace(" ", "_").lower()}.joblib'
    joblib.dump(model, model_path)
    print(f" Saved {name} model to {model_path}")

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title(f'Confusion Matrix: {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    cm_path = f'model_evaluation/confusion_matrix_{name.replace(" ", "_").lower()}.png'
    plt.savefig(cm_path)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")

df_results = pd.DataFrame(results)
results_csv_path = 'model_evaluation/model_comparison.csv'
df_results.to_csv(results_csv_path, index=False)

print("\n Model Evaluation Complete. Results saved to:")
print(f"  {results_csv_path}\n")
print(df_results)
