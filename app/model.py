from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pickle, os

def train_and_save_model():
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    return model

def load_model():
    if not os.path.exists('model.pkl'):
        return train_and_save_model()
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)