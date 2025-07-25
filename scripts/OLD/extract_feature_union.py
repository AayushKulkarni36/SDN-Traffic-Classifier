import pandas as pd
import os
from functools import reduce

dataset_paths = [
    'datasets/dns_training_data.csv',
    'datasets/game_training_data.csv',
    'datasets/ping_training_data.csv',
    'datasets/telnet_training_data.csv',
    'datasets/voice_training_data.csv'
]

print("Extracting union of feature columns from raw CSVs...")

all_columns = []

for path in dataset_paths:
    df = pd.read_csv(path)
    df.drop(columns=['Traffic Type'], errors='ignore', inplace=True)
    df = pd.get_dummies(df)
    all_columns.append(set(df.columns))


master_features = sorted(reduce(lambda a, b: a.union(b), all_columns)) 


pd.Series(master_features).to_csv('scripts/feature_list.csv', index=False, header=False)  
print(f"Master feature list saved to scripts/feature_list.csv with {len(master_features)} columns")
