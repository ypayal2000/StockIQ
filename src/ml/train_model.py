import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

# from src.utils.logger import logger


class StockModelTrainer:

    def load_data(self):
        return pd.read_csv("data/ml_dataset.csv")

    def prepare_features(self, df):

        features = ["close", "moving_avg_3", "daily_return_pct", "volatility"]

        X = df[features]
        y = df["target"]

        return X, y

    def train(self):

        print("Loading dataset...")

        df = self.load_data()

        X, y = self.prepare_features(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        print(f"\nTraining Rows: {len(X_train)}")
        print(f"Testing Rows: {len(X_test)}")

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42
        )

        print("\nTraining model...")

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        print("\nModel Evaluation")
        print("-" * 40)

        print(f"Accuracy  : {accuracy_score(y_test, predictions):.4f}")
        print(f"Precision : {precision_score(y_test, predictions):.4f}")
        print(f"Recall    : {recall_score(y_test, predictions):.4f}")
        print(f"F1 Score  : {f1_score(y_test, predictions):.4f}")
        print(f"ROC AUC   : {roc_auc_score(y_test, probabilities):.4f}")

        print("\nClassification Report")
        print(classification_report(y_test, predictions))

        os.makedirs("src/ml/models", exist_ok=True)

        model_path = ("src/ml/models/stock_predictor.pkl")

        joblib.dump(model, model_path)

        print(f"\nModel saved to: {model_path}")

        return model


if __name__ == "__main__":

    trainer = StockModelTrainer()

    trainer.train()