import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from utils.data_loader import load_dataset, split_features_labels
from utils.feature_engineering import scale_features, save_scaler
from utils.evaluation import evaluate_model
from config import DATASET_PATH, MODEL_PATH


def train():

    # Load dataset
    data = load_dataset(DATASET_PATH)

    # Split features and labels
    X, y = split_features_labels(data)

    # Scale features
    X_scaled = scale_features(X)

    # Save scaler
    save_scaler("model/scaler.pkl")

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    # Create model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    acc, report = evaluate_model(model, X_test, y_test)

    print("Model Accuracy:", acc)
    print(report)

    # Save model
    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully")


if __name__ == "__main__":
    train()