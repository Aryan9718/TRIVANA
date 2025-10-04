import random

def mock_predict():
    prob = round(random.uniform(0.6, 0.98), 3)
    return {
        "planet_detected": prob > 0.7,
        "probability": prob,
        "orbital_period": round(random.uniform(1.0, 30.0), 3),
        "radius": round(random.uniform(0.5, 2.5), 3)
    }
