#!/usr/bin/python
# -*- coding: utf-8 -*-

# train_test_split.py

import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.svm import LinearSVC, SVC

from create_lagged_series import create_lagged_series


def run_models(X_train, X_test, y_train, y_test):
    # Define the models
    models = {
        "Logistic Regression": LogisticRegression(),
        "LDA": LDA(),
        "QDA": QDA(),
        "Linear SVC": LinearSVC(),
        "SVM (RBF Kernel)": SVC(
            C=1000000.0, gamma=0.0001, kernel='rbf'
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=1000, max_features='sqrt'
        )
    }

    # Iterate through the models
    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        pred = model.predict(X_test)

        # Output the hit-rate and the confusion matrix for each model
        print(f"{name}:\n{model.score(X_test, y_test):.3f}")
        print(f"{confusion_matrix(pred, y_test)}\n")


if __name__ == "__main__":
    # Create a lagged series of the S&P500 US stock market index
    snpret = create_lagged_series(
        "^GSPC", datetime.datetime(2001, 1, 10),
        datetime.datetime(2005, 12, 31), lags=5
    )

    # Use the prior two days of returns as predictor values, with direction as the response
    X = snpret[["Lag1", "Lag2"]]
    y = snpret["Direction"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.8, random_state=42
    )

    # Run models and print results
    print("Hit Rates/Confusion Matrices:\n")
    run_models(X_train, X_test, y_train, y_test)
