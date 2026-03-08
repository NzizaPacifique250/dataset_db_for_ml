# Task 4 – User Guide (Traditional Machine Learning Prediction)

## 1. Overview

Task 4 demonstrates how to use a **trained Traditional Machine Learning model (Linear Regression)** to predict **traffic volume** using a record retrieved from the database through an API.

The script:

1. Retrieves a **single traffic record** from the API.
2. Preprocesses the data to match the training pipeline.
3. Loads the trained **Linear Regression model**.
4. Generates a prediction.
5. Compares the predicted traffic volume with the **actual value** and computes the **RMSE**.

The script used for this task is:

```
ml_script1.py
```

---

# 2. Required Python Packages

Install the required packages inside a virtual environment.

```bash
pip install pandas
pip install numpy
pip install requests
pip install scikit-learn
pip install joblib
```

These packages are used for:

| Package      | Purpose              |
| ------------ | -------------------- |
| pandas       | Data processing      |
| numpy        | Numerical operations |
| requests     | API calls            |
| scikit-learn | Model metrics        |
| joblib       | Loading saved models |

---

# 3. Project Dependencies

Before running Task 4, the following tasks must already be running.

---

## Task 2 – Database Setup

Task 2 creates and populates the **traffic database**.

Steps:

1. Start MySQL.
2. Run the SQL schema file.
3. Import the dataset into the database.

The following tables must exist:

* `traffic`
* `datetime_info`
* `holiday_info`
* `weather_info`

---

## Task 3 – API Service

Task 3 provides the API used to retrieve records from the database.

Start the API server using:

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

Task 4 uses the following endpoint:

### MySQL Endpoint

```
http://127.0.0.1:8000/mysql/single?date_time=YYYY-MM-DD%20HH:MM:SS
```

### MongoDB Endpoint

```
http://127.0.0.1:8000/mongo/single?date_time=YYYY-MM-DD%20HH:MM:SS
```

This endpoint returns **one traffic record for the specified datetime**.

---

# 4. Datetime Used for Testing

The datetime selected for retrieving a record was:

```
2018-09-30 19:00:00
```

Encoded version used in the API:

```
2018-09-30%2019%3A00%3A00
```

Example API call:

```
http://127.0.0.1:8000/mysql/single?date_time=2018-09-30%2019%3A00%3A00
```

---

# 5. Running the Script

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the prediction script:

```bash
python ml_script1.py
```

The script will:

1. Request the record from the API.
2. Convert it into a DataFrame.
3. Drop unnecessary columns.
4. Encode categorical variables.
5. Align features with the model training columns.
6. Load the trained **Linear Regression model**.
7. Generate a prediction.
8. Calculate **RMSE**.

---

# 6. Files Required

Ensure the following files exist in the project directory:

```
ml_script1.py
linear_regression_model.pkl
```

Optional files used during training:

```
input_columns.pkl
```

---

# 7. Prediction results


Prediction result:

| True_Y | Predicted_Y | RMSE  |
| ------ | ----------- | ----- |
| 3543   | 2588        | 955.00 |

---

# 8. Result Interpretation

| Metric      | Meaning                                |
| ----------- | -------------------------------------- |
| True_Y      | Actual traffic volume from the dataset |
| Predicted_Y | Model prediction                       |
| RMSE        | Root Mean Squared Error                |

A **lower RMSE** indicates better prediction accuracy.

---

# 9. Summary

Task 4 integrates:

* Database retrieval (Task 2)
* API data access (Task 3)
* Traditional Machine Learning prediction