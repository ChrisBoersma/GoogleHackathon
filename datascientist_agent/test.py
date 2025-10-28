import pandas as pd
from agent import get_train_data, predict_using_random_forest
import json

# 1. Get the training data
#train_data = get_train_data()

# 2. Create a decision tree
#clf, encoders = x(train_data)

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

patient_json = [
    {
        "L-CORE": "mid",
        "L-SURF": "low",
        "L-O2": "excellent",
        "L-BP": "mid",
        "SURF-STBL": "stable",
        "CORE-STBL": "stable",
        "BP-STBL": "stable",
        "COMFORT": 15,
        "Name": ""
    }
]

# 4. Use the y function to predict the outcome
#prediction = y(clf, encoders, patient_data.to_json())

# 5. Print the prediction
#print(prediction)

#patient_data = ''
train_data_path = get_train_data('post-operative-data-with-names.csv')
json_string = json.dumps(patient_json)
print(predict_using_random_forest(train_data_path, json_string, 'decision ADM-DECS'))
