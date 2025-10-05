"""Utility helpers for loading data, preprocessing, training and evaluation.

This module implements generic functions used by both train.py and train2.py
so the assignment requirements (re-use of functions) are satisfied.
"""
from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler


def load_data() -> pd.DataFrame:
    """Download the (deprecated) Boston housing dataset and return as DataFrame."""
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)

    data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    target = raw_df.values[1::2, 2]

    feature_names = [
        'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE',
        'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT'
    ]

    df = pd.DataFrame(data, columns=feature_names)
    df['MEDV'] = target
    return df


def split_features_target(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Return X, y arrays from the DataFrame."""
    X = df.drop(columns=['MEDV']).values.astype(float)
    y = df['MEDV'].values.astype(float)
    return X, y


def train_test_split_data(X: np.ndarray, y: np.ndarray, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def scale_data(X_train: np.ndarray, X_test: np.ndarray):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def cross_val_score_avg(model, X: np.ndarray, y: np.ndarray, cv=5, scoring=None, random_state=42):
    """Perform K-Fold cross-validation and return the average score.

    scoring should be a callable that accepts (y_true, y_pred) and returns a scalar.
    If scoring is None, uses model.score on folds.
    """
    kf = KFold(n_splits=cv, shuffle=True, random_state=random_state)
    scores = []
    for train_idx, test_idx in kf.split(X):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        if scoring is None:
            scores.append(model.score(X_te, y_te))
        else:
            scores.append(scoring(y_te, preds))
    return np.mean(scores), np.array(scores)


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, metric):
    preds = model.predict(X_test)
    return metric(y_test, preds)
