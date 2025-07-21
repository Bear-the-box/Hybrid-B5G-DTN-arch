import flwr as fl
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from utils import load_client_data
import matplotlib.pyplot as plt
import joblib

class FLClient(fl.client.NumPyClient):
    def __init__(self, model, X_train, y_train, X_test, y_test):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def get_parameters(self, config):
        return [self.model.coef_, self.model.intercept_]

    def fit(self, parameters, config):
        self.model.coef_ = parameters[0]
        self.model.intercept_ = parameters[1]
        self.model.fit(self.X_train, self.y_train)
        return self.get_parameters(config), len(self.X_train), {}

    def evaluate(self, parameters, config):
        self.model.coef_ = parameters[0]
        self.model.intercept_ = parameters[1]

        y_pred = self.model.predict(self.X_test)

        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)

        print(f"\n--- Evaluation Metrics ---")
        print(f"MSE:  {mse:.6f}")
        print(f"RMSE: {rmse:.6f}")
        print(f"MAE:  {mae:.6f}")
        print(f"R²:   {r2:.6f}")
        print(f"--------------------------\n")

        plt.figure(figsize=(6, 6))
        plt.scatter(self.y_test, y_pred, alpha=0.6)
        plt.plot([min(self.y_test), max(self.y_test)], [min(self.y_test), max(self.y_test)], 'r--')
        plt.xlabel("Actual Score")
        plt.ylabel("Predicted Score")
        plt.title("Prediction vs Actual")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return mse, len(self.X_test), {}

def start_client(file_path):
    X_train, X_test, y_train, y_test = load_client_data(file_path)
    model = SGDRegressor()

    try:
        model.partial_fit(X_train[:1], y_train[:1])
    except:
        model.partial_fit(np.random.rand(2, X_train.shape[1]), np.random.rand(2))

    joblib.dump(model, "score_model.pkl")

    client = FLClient(model, X_train, y_train, X_test, y_test)
    fl.client.start_client(
        server_address="localhost:8080",
        client=client.to_client()
    )



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python client.py <path_to_csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    start_client(file_path)

