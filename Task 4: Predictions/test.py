cols_api = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'is_weekend', 'lag_1',
       'lag_24', 'lag_168', 'rolling_mean_24', 'rolling_mean_168',
       'holiday_Columbus Day', 'holiday_Independence Day', 'holiday_Labor Day',
       'holiday_Martin Luther King Jr Day', 'holiday_Memorial Day',
       'holiday_New Years Day', 'holiday_No', 'holiday_State Fair',
       'holiday_Thanksgiving Day', 'holiday_Veterans Day',
       'holiday_Washingtons Birthday', 'weather_main_Clouds',
       'weather_main_Drizzle', 'weather_main_Fog', 'weather_main_Haze',
       'weather_main_Mist', 'weather_main_Rain', 'weather_main_Smoke',
       'weather_main_Snow', 'weather_main_Squall', 'weather_main_Thunderstorm',
       'day_of_week_1', 'day_of_week_2', 'day_of_week_3', 'day_of_week_4',
       'day_of_week_5', 'day_of_week_6']

cols_model = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'year', 'month', 'day',
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


cols_test = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'year', 'month', 'day',
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


import joblib  # for loading pickle files
# 5️⃣ Load Saved Columns and Align
with open('input_columns.pkl', 'rb') as f:
    saved_columns = joblib.load(f)

print(len(saved_columns))
print(len(cols_model))
print(len(cols_test))
