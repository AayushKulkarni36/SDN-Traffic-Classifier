import pandas as pd
from imblearn.over_sampling import SMOTE
df = pd.read_csv('/home/aayush/sdn-traffic-classifier/scripts/new/refined_dataset_with_malicious.csv')

df_clean = df.dropna()

X = df_clean.drop('Label', axis=1)
y = df_clean['Label']


sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X, y)

df_balanced = pd.DataFrame(X_resampled, columns=X.columns)
df_balanced['Label'] = y_resampled


balanced_path = '/home/aayush/sdn-traffic-classifier/scripts/new/balanced_dataset.csv'
df_balanced.to_csv(balanced_path, index=False)

print(df_balanced['Label'].value_counts())
print(f"\nBalanced dataset saved to: {balanced_path}")
