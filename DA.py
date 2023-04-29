import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris


def pls_da(X_train, y_train, X_test, th = 0.5):
    # Define the PLS object
    pls_binary = PLSRegression(n_components = 2)

    # Calculate coefficients
    pls_binary.fit(X_train, y_train)
    print (pls_binary.coef_)

    # Predictions: these won't generally be integer numbers
    y_pred = pls_binary.predict(X_test)[:, 0]

    # "Force" binary prediction by thresholding
    binary_prediction = (y_pred > th).astype('uint8')
    return binary_prediction

def pls_da1(X_train, y_train, X_test, th = 0.5):
    # Define the PLS object
    pls_binary = PLSRegression(n_components = 2)

    # Calculate coefficients
    pls_binary.fit(X_train, y_train)
    return pls_binary.coef_



if __name__=="__main__":
        
    # Load data
    data = load_iris()
    y_binary = data.target
    data = data.data
    print (data.shape, y_binary.shape)

    # Create train-test split
    X_train, X_test, y_train, y_test = train_test_split(data, y_binary, test_size=0.2, random_state=19)

    # Make predictions
    binary_prediction = pls_da(X_train, y_train, X_test)
    print (binary_prediction)

    # Test accuracy
    accuracy = []
    cval = KFold(n_splits=20, shuffle=True, random_state=19)
    for train, test in cval.split(data):
        y_pred = pls_da(data[train, :], y_binary[train], data[test, :])
        accuracy.append(accuracy_score(y_binary[test], y_pred))
    print("Average accuracy on 10 splits: ", np.array(accuracy).mean())
