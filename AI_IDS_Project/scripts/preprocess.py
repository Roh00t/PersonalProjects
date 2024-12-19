import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(data):
    # Strip extra quotes from column names
    data.columns = data.columns.str.strip("'")

    # Verify required columns
    required_columns = ['protocol_type', 'service', 'flag']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing column: {col}")

    # Encode categorical features
    label_enc = LabelEncoder()
    data['protocol_type'] = label_enc.fit_transform(data['protocol_type'])
    data['service'] = label_enc.fit_transform(data['service'])
    data['flag'] = label_enc.fit_transform(data['flag'])
    
    # Normalize numerical features
    features = data.iloc[:, :-1]  # Exclude label
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    labels = data.iloc[:, -1].copy()  # Only label
    labels = labels.apply(lambda x: 0 if x == 'normal' else 1)  # Binary classification
    return features_scaled, labels