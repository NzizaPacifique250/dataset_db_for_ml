# User Guide — Task 1: Time-Series Data Preparation & Model Training

## 1. Project Overview

**Goal:** Predict hourly traffic volume using historical traffic and weather data to support smarter transportation planning.

**Dataset:** [Metro Interstate Traffic Volume](https://www.kaggle.com/datasets/mikedev/metro-traffic-volume) (2012–2018, hourly)

**Problem Justification:**
- Traffic congestion affects city mobility.
- Forecasting helps traffic control and infrastructure planning.

---

## 2. Dataset Overview

| Column | Description |
|--------|-------------|
| holiday | Holiday indicator |
| temp | Temperature |
| rain_1h | Rainfall last hour |
| snow_1h | Snowfall last hour |
| clouds_all | Cloud coverage |
| weather_main | Main weather condition |
| weather_description | Detailed weather condition (dropped) |
| date_time | Timestamp |
| traffic_volume | Target variable |

---

## 3. Data Preprocessing

**Steps:**

1. Fill missing `holiday` values with `"No"`.  
2. Convert `date_time` to datetime type.  
3. Extract time features: year, month, day, hour, day_of_week, is_weekend.  
4. Add lag features: `lag_1`, `lag_24`, `lag_168`.  
5. Add rolling averages: `rolling_mean_24`, `rolling_mean_168`.  
6. Drop unnecessary columns (`weather_description`).  
7. Drop rows with missing values after lag/rolling operations.  
8. Encode categorical features (`holiday`, `weather_main`, `day_of_week`).  
9. Drop unused time columns before modeling.  
10. Scale features if using LSTM.

---

## 4. Exploratory Data Analysis (EDA)

**Key Insights:**

- Time range: **2012–2018**, hourly frequency.  
- Traffic patterns show **daily and weekly trends**.  
- Weekdays have morning (8 AM) and evening (4 PM) peaks.  
- Weekends have a single peak around noon.  
- Temperature correlates positively with traffic; rain/snow show negative correlation.

**Placeholders for Graphs:**

- Traffic Volume Hour Of Day
<img width="1014" height="547" alt="traffic volume by hour of day" src="https://github.com/user-attachments/assets/4a15bc61-83b9-4e30-a5ec-9993df020a58" />


- Daily Traffic Trend: Weekday vs Weekend and Traffic by Day of Week  
<img width="1589" height="590" alt="traffic volume over time" src="https://github.com/user-attachments/assets/6aa76915-0182-483a-9fdf-6cd3c5198891" />


- Correlation Matrix: Traffic vs External Variables
<img width="1589" height="590" alt="traffic volume over time" src="https://github.com/user-attachments/assets/eb58b4df-31e2-4a57-8108-d8e301d0b8f6" />


---

## 5. Analytical Questions

1. Does traffic volume show an increasing/decreasing trend?  
2. Does traffic have daily patterns?  
3. Do external variables correlate with traffic?  
4. Is traffic lower on weekends?  
5. How do lagged features (1-hour, 24-hour, 168-hour) predict traffic?

*Visualizations for each question are included in placeholders above.*

---

## 6. Model Training

**Models Trained:**

| Model Type | Library | Notes |
|------------|---------|-------|
| Linear Regression | scikit-learn | Traditional baseline |
| LSTM Neural Network | TensorFlow/Keras | Deep learning for sequential data |

**Training Notes:**

- Hyperparameter tuning performed for both models.  
- Features scaled for LSTM.  
- Lag and rolling features included.

**Placeholders for Results Table:**

| Experiment | Model | Hyperparameters | MSE | R² |
|------------|-------|----------------|-----|----|
| 1 | Linear Regression | Default | 692.573 | 0.878 |
| 2 | LSTM | 1 | 64 | 496.023 | 0.937 |

---

## 7. Summary

The Task 1 pipeline includes:

1. Dataset exploration  
2. Missing value handling  
3. Feature engineering (time-based, lag, rolling)  
4. Exploratory analysis with visualization  
5. Model training (traditional + deep learning)  
6. Hyperparameter tuning and comparison

---
