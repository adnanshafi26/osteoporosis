from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler()

def scale_features(X):

    X_scaled = scaler.fit_transform(X)

    return X_scaled


def save_scaler(path):
    joblib.dump(scaler, path)


def load_scaler(path):
    return joblib.load(path)