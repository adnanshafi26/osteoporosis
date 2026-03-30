from utils.data_loader import load_dataset, split_features_labels
from utils.feature_engineering import scale_features
from sklearn.model_selection import train_test_split

def preprocess_data(dataset_path):

    data = load_dataset(dataset_path)

    X, y = split_features_labels(data)

    X_scaled = scale_features(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test