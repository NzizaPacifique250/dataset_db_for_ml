# lstm_prediction_api.py
import pandas as pd
import numpy as np
import requests
import joblib
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

# Saved training columns
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

def predict_single_record(source: str, date_time_str: str):
    """
    Fetch one record from either MongoDB or MySQL API, preprocess, and make prediction.
    
    Args:
        source (str): 'mongodb' or 'mysql'
        date_time_str (str): datetime string, e.g., '2018-09-30 19:00:00'
    
    Returns:
        pd.DataFrame: table with True Y, Predicted Y, RMSE, R2
    """

    # -------------------------------
    # 1️⃣ Choose API endpoint
    # -------------------------------
    if source.lower() == "mongodb":
        url = f"http://127.0.0.1:8000/mongo/single?date_time={date_time_str}"
        unnecessary_cols = ['_id', 'date_time']
    elif source.lower() == "mysql":
        url = f"http://127.0.0.1:8000/mysql/single?date_time={date_time_str}"
        unnecessary_cols = ['primary_id', 'date_time']
    else:
        raise ValueError("source must be 'mongodb' or 'mysql'")

    # -------------------------------
    # 2️⃣ Fetch data from API
    # -------------------------------
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data_json = response.json()
    record = data_json
    print("Raw record:", record)

    # -------------------------------
    # 3️⃣ Convert to DataFrame
    # -------------------------------
    df = pd.DataFrame([record])

    # Drop unnecessary columns
    X = df.drop("traffic_volume", axis=1)
    y = df['traffic_volume']
    X.drop(columns=[col for col in unnecessary_cols if col in X.columns], inplace=True)

    # -------------------------------
    # 4️⃣ Encode categorical columns
    # -------------------------------
    X = pd.get_dummies(X, columns=['holiday', 'weather_main', 'day_of_week'], drop_first=True)

    # -------------------------------
    # 5️⃣ Align with saved columns
    # -------------------------------
    for col in saved_columns:
        if col not in X.columns:
            X[col] = 0
    X = X[saved_columns]

    # -------------------------------
    # 6️⃣ Load traditional model and predict
    # -------------------------------
    traditional_model = joblib.load('linear_regression_model.pkl')
    y_pred_traditional = traditional_model.predict(X)

    # -------------------------------
    # 7️⃣ Compute metrics
    # -------------------------------
    mse_lr = np.sqrt(mean_squared_error(y, y_pred_traditional))
    # r2_lr = r2_score(y, y_pred_traditional)

    # -------------------------------
    # 8️⃣ Build result table
    # -------------------------------
    result_df = pd.DataFrame({
        "True_Y": y.values,
        "Predicted_Y": y_pred_traditional,
        "RMSE": [mse_lr],
        # "R2": [r2_lr]
    })

    return result_df


# Example usage
if __name__ == "__main__":
    date_time_example = "2018-09-30 19:00:00"
    result = predict_single_record("mysql", date_time_example)
    print(result)