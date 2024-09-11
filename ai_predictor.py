import numpy as np

def predict_stock(symbols):
    predictions = {}
    for symbol in symbols:
        # Simulated prediction logic
        predictions[symbol] = np.random.uniform(100, 150)
    return predictions
