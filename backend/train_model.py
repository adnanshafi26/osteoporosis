import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("osteoporosis_dataset_10000_final.csv")

# Features & target
X = df[['age', 'gender', 'bmi', 'bone_density', 'calcium', 'vitamin_d', 'bone_type']]
y = df['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Accuracy
print("Accuracy:", model.score(X_test, y_test))

# Save model
joblib.dump(model, "osteoporosis_model.pkl")