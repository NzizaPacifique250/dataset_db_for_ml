# 1️⃣ Import Packages
import pandas as pd
import numpy as np
import requests
import json
from sklearn.metrics import mean_squared_error, r2_score

import joblib  # for loading pickle files
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from datetime import datetime
# from tensorflow.keras.models import load_model  # for advanced model (.h5)


# Read Data (Single Record Example)
saved_columns = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'year', 'month', 'day',
       'is_weekend', 'hour', 'lag_1', 'lag_24', 'lag_168', 'rolling_mean_24',
       'rolling_mean_168', 'holiday_Columbus Day', 'holiday_Independence Day',
       'holiday_Labor Day', 'holiday_Martin Luther King Jr Day',
       'holiday_Memorial Day', 'holiday_New Years Day', 'holiday_No',
       'holiday_State Fair', 'holiday_Thanksgiving Day',
       'holiday_Veterans Day', 'holiday_Washingtons Birthday',
       'weather_main_Clouds', 'weather_main_Drizzle', 'weather_main_Fog',
       'weather_main_Haze', 'weather_main_Mist', 'weather_main_Rain',
       'weather_main_Smoke', 'weather_main_Snow', 'weather_main_Squall',
       'weather_main_Thunderstorm', 'day_of_week_1', 'day_of_week_2',
       'day_of_week_3', 'day_of_week_4', 'day_of_week_5', 'day_of_week_6']

# mongodb
# url = "http://127.0.0.1:8000/mongo/single?date_time=2018-09-30%2019%3A00%3A00"

# sql
url = "http://127.0.0.1:8000/mysql/single?date_time=2018-09-30%2019%3A00%3A00"  # replace with your API endpoint
response = requests.get(url)
data_json = response.json()

# Extract only the latest record
record = data_json
print("Raw record:", record)

# 3️⃣ Convert to Clean Structure (Remove Unnecessary Columns)
df = pd.DataFrame([record])

# sql
unnecessary_cols = ['primary_id', 'date_time']  

# mongodb
# unnecessary_cols = ['_id', 'date_time']

# convert X and y
X = df.drop("traffic_volume", axis=1)
y = df['traffic_volume']


X.drop(columns=[col for col in unnecessary_cols if col in df.columns], inplace=True)

# 4️⃣ Encode Categorical Columns
X = pd.get_dummies(X, columns=['holiday', 'weather_main', 'day_of_week'], drop_first=True)

# # 5️⃣ Load Saved Columns and Align
# with open('input_columns.pkl', 'rb') as f:
#     saved_columns = joblib.load(f)


# Add missing columns with 0
for col in saved_columns:
    if col not in X.columns:
        X[col] = 0
X = X[saved_columns]  # reorder to match training



# Make  prediction using Traditional M
traditional_model = joblib.load('linear_regression_model.pkl')
y_pred_traditional = traditional_model.predict(X)
print("Traditional model prediction:", y_pred_traditional)

mse_lr = np.sqrt(mean_squared_error(y, y_pred_traditional))
r2_lr = r2_score(y, y_pred_traditional)



print("-------------------------------------")
print(f'True Y: {y}')
print(f'Predicted Y: {y_pred_traditional}')
print(f'MSE Y: {mse_lr}')
print(f'R2_score {r2_lr}')
print("-------------------------------------")



# # what we are going to do
# 1. Import packages
# 2. read the data using the return single record using datetime, requests
# 3. Convert to a clean structure(remove unccessary cols)
# 4. Encode categorical columns
# 5. Load saved columns and compare
# 6. Load saved scaler and scale numerical values
# 7. Load Traditional model and make prediction
# 8. Load advanced model and make prediction
# 9. calculate the MSE on actual y and predicted