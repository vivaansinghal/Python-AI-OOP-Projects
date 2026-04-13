import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


class ShuttleTelemetryAnalyzer:
    """An OOP wrapper for an aerospace sensor classification pipeline."""
   
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.feature_names = []


    def load_and_prep_data(self) -> None:
        """Fetches the real Space Shuttle dataset from OpenML."""
        print("Fetching Space Shuttle dataset...")
        # Fetching dataset ID 40685 (Statlog Shuttle)
        shuttle = fetch_openml(name='shuttle', version=1, as_frame=True, parser='auto')
        df = shuttle.frame
       
        # The dataset has classes 1-7. Class 1 is 'Rad Flow' (Nominal).
        # We will binarize: 1 = Nominal (0), Others = Anomaly (1)
        X = df.drop('class', axis=1)
        y = np.where(df['class'] == '1', 0, 1)
       
        self.feature_names = X.columns.tolist()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print("Data preparation complete.")


    def train_model(self) -> None:
        if self.X_train is None:
            raise ValueError("Data not loaded. Call load_and_prep_data() first.")
        print("Training Random Forest Classifier on sensor data...")
        self.model.fit(self.X_train, self.y_train)


    def evaluate(self) -> None:
        predictions = self.model.predict(self.X_test)
        print("\n--- Classification Report ---")
        print(classification_report(self.y_test, predictions, target_names=["Nominal", "Anomaly"]))
       
    def plot_feature_importance(self) -> None:
        """Uses matplotlib to visualize which sensors contribute most to anomalies."""
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]


        plt.figure(figsize=(10, 6))
        plt.title("Sensor Importance in Anomaly Detection (Space Shuttle)")
        plt.bar(range(self.X_train.shape[1]), importances[indices], align="center", color='steelblue')
        plt.xticks(range(self.X_train.shape[1]), [self.feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        plt.savefig("feature_importance.png")
        print("Plot saved as 'feature_importance.png'.")


# --- Execution ---
if __name__ == "__main__":
    analyzer = ShuttleTelemetryAnalyzer()
    analyzer.load_and_prep_data()
    analyzer.train_model()
    analyzer.evaluate()
    analyzer.plot_feature_importance()

