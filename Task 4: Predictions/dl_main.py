"""
# 1️⃣ Import Packages
import pandas as pd
import numpy as np
import requests
import json
from sklearn.metrics import mean_squared_error, r2_score

import joblib  # for loading pickle files
from sklearn.metrics import mean_squared_error
from datetime import datetime
from tensorflow.keras.models import load_model  # for advanced model (.h5)




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
# url = "http://127.0.0.1:8000/mongo/last24?date_time=2018-09-30%2019%3A00%3A00"

# sql
url = "http://127.0.0.1:8000/mysql/last24?date_time=2018-09-30%2019%3A00%3A00"  # replace with your API endpoint
response = requests.get(url)
data_json = response.json()

df = pd.DataFrame([data_json])
print("Raw last 24 records:")
print(df)
print(len(df))
if len(data_json) < 24:
    raise ValueError("Not enough records (need 24) to make LSTM prediction")

df = pd.DataFrame(data_json)
print("Raw last 24 records:")
print(df)

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

scaler_X = joblib.load("scaler_X.pkl")
scaler_y = joblib.load("scaler_y.pkl")

X_scaled = scaler_X.transform(X)
y_scaled = scaler_y.transform(y.values.reshape(-1, 1))

# -------------------------------
# 6️⃣ Create LSTM sequence (1 sample, 24 timesteps)
# -------------------------------
time_steps = 24
X_seq = X_scaled.reshape(1, time_steps, X_scaled.shape[1])
y_seq = y_scaled.reshape(1, time_steps)  # optional for debugging


# -------------------------------
# 7️⃣ Load LSTM model and make predictions
# -------------------------------
lstm_model = load_model("LTSM_model.h5", compile=False)
y_pred_scaled = lstm_model.predict(X_seq)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_true = scaler_y.inverse_transform(y_seq)

# -------------------------------
# 8️⃣ Build results table
# -------------------------------
results_df = pd.DataFrame({
    "y_true": y_true.flatten(),
    "y_pred": y_pred.flatten()
})

rmse_lstm2 = np.sqrt(mean_squared_error(y_true, y_pred))
r2_lstm2 = r2_score(y_true, y_pred)

results_df["rmse_lstm2"] = rmse_lstm2
results_df["r2_lstm2"] = r2_lstm2

print("\nPrediction Results:")
print(results_df)
print(f"\nRMSE: {rmse_lstm2:.2f}, R2: {r2_lstm2:.4f}")
"""
