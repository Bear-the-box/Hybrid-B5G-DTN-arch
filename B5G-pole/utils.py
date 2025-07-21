import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_client_data(file_path):
    df = pd.read_csv(file_path)
    features = [
        "timestamp",
        "host1",
        "host2",
        "duration",
        "buffer_availability",
        "battery_level",
        "delivered",
        "hoplist",
        "contactedDestination"
    ]
    target = "score"

    df = df[features + [target]].dropna()
    X = df[features]
    y = df[target]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
