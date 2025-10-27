import pandas as pd
from agent import get_train_data, x, y

# 1. Get the training data
train_data = get_train_data()

# 2. Create a decision tree
clf, encoders = x(train_data)

# 3. Create a sample patient data
patient_data = pd.DataFrame({
    'L-CORE': ['mid'],
    'L-SURF': ['low'],
    'L-O2': ['excellent'],
    'L-BP': ['mid'],
    'SURF-STBL': ['stable'],
    'CORE-STBL': ['stable'],
    'BP-STBL': ['stable'],
    'COMFORT': [15]
})

# 4. Use the y function to predict the outcome
prediction = y(clf, encoders, patient_data.to_json())

# 5. Print the prediction
print(prediction)
