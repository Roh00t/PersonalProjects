# Import libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Load the dataset
def load_data(train_path, test_path):
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    return train_data, test_data

# Preprocess the dataset
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

# Train Isolation Forest
def train_isolation_forest(X_train):
    model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42) # Hyperparameter Tuning, n_estimators: Increase the number of trees (e.g., 200 or 300) for better feature separation. contamination: Set a more accurate contamination value based on your dataset’s anomaly proportion.
#    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42) # DEFAULT Isolation Forest Behaviour
    model.fit(X_train)
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    predictions = np.where(predictions == -1, 1, 0)  # Convert to binary format
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("Classification Report:\n", classification_report(y_test, predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    return predictions

# Visualize results
def plot_results(X_test, predictions):
    plt.scatter(X_test[:, 0], X_test[:, 1], c=predictions, cmap='coolwarm', alpha=0.7)
    plt.title('Intrusion Detection Results')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.colorbar(label='Anomaly (1) vs Normal (0)')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Load datasets
    train_data, test_data = load_data("../data/KDDTrain+.csv", "../data/KDDTest+.csv")
    
    # Preprocess datasets
    X_train, y_train = preprocess_data(train_data)
    X_test, y_test = preprocess_data(test_data)
    
    # Train the model
    print("Training Isolation Forest...")
    model = train_isolation_forest(X_train)
    
    # Evaluate the model
    print("Evaluating model...")
    predictions = evaluate_model(model, X_test, y_test)
    
    # Visualize results
    print("Visualizing results...")
    plot_results(X_test, predictions)
