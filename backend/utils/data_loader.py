import pandas as pd

def load_dataset(path):
    """
    Load bone density dataset
    """
    data = pd.read_csv(path)
    return data


def split_features_labels(data):
    """
    Separate features and labels
    """
    X = data.drop("Osteoporosis", axis=1)
    y = data["Osteoporosis"]

    return X, y