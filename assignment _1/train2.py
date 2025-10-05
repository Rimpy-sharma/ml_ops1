"""Train a KernelRidge model on the Boston housing dataset.

Uses the same helper functions in `misc.py` so code is reusable across models.
"""
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
import numpy as np

from misc import load_data, split_features_target, train_test_split_data, scale_data


def main(random_state=42):
    df = load_data()
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split_data(X, y, random_state=random_state)
    X_train_s, X_test_s, scaler = scale_data(X_train, X_test)

    model = KernelRidge(alpha=1.0, kernel='rbf')
    model.fit(X_train_s, y_train)
    preds = model.predict(X_test_s)
    mse = mean_squared_error(y_test, preds)
    print(f"KernelRidge MSE: {mse:.4f}")


if __name__ == '__main__':
    main()
