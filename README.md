# Traffic Volume Prediction: Time-Series ML Pipeline

A complete end-to-end machine learning pipeline for predicting hourly traffic volume using time-series data. This project demonstrates data preprocessing, dual-database implementation (MySQL & MongoDB), RESTful API development, and model deployment for real-time predictions.

## 📊 Project Overview

This project uses the [Metro Interstate Traffic Volume dataset](https://www.kaggle.com/datasets/mikedev/metro-traffic-volume) from Kaggle to predict hourly traffic volume based on weather conditions, holidays, and temporal patterns. The pipeline integrates classical machine learning (Linear Regression) and deep learning (LSTM) approaches with production-ready database and API infrastructure.

**Dataset Features:**
- **Time Range:** 2012-2018 (hourly frequency)
- **Target Variable:** Traffic volume (vehicles per hour)
- **Features:** Temperature, precipitation, cloud coverage, weather conditions, holidays, and engineered lag/rolling features

---

## 🏗️ Project Structure

```
dataset_db_for_ml/
├── Task 1_  EDA and model training/
│   ├── Building_a_Pipeline_for_Time_Series_Data.ipynb
│   ├── Automobile_data.csv
│   ├── LTSM_model.h5
│   ├── linear_regression_model.pkl
│   └── USER_GUIDE.md
├── Task 2_ databases_updated/
│   ├── mysql/
│   │   ├── mysql_schema.sql
│   │   ├── clean_data_load.py
│   │   ├── mysql_crud.py
│   │   └── ERD_diagram.md
│   └── mongodb/
│       ├── mongo_schema.py
│       └── mongo_crud.py
├── Task 3_ API_updated/
│   ├── main.py
│   ├── mysql_crud_api.py
│   ├── mongodb_crud_api.py
│   ├── requirements.txt
│   └── README.md
└── Task 4_ Predictions/
    ├── ml_main.py
    ├── dl_main.py
    ├── ml_script1.py
    └── USER_GUIDE.md
```

---

## 👥 Contributors

| Task | Contributor | Responsibility |
|------|-------------|----------------|
| **Task 1: EDA & Model Training** | Emmanuella Asoliya Briggs | Exploratory data analysis, feature engineering, and training Linear Regression + LSTM models |
| **Task 2: Database Design** | Nziza Aime Pacifique | Designing and implementing MySQL (normalized) and MongoDB (denormalized) schemas with data loading |
| **Task 3: API Development** | Kayonga Elvis | Building FastAPI CRUD endpoints for both databases with time-series query support |
| **Task 4: Prediction Pipeline** | Kevin Mike Chris Ntwari | API integration and inference scripts for ML/DL model predictions |

---

## 🚀 Tasks Overview

### **Task 1: Exploratory Data Analysis & Model Training**
**Lead:** Emmanuella Asoliya Briggs

Comprehensive time-series analysis and model development:
- **Data Preprocessing:** Handled missing values, extracted temporal features (year, month, day, hour, day_of_week, is_weekend)
- **Feature Engineering:** Created lag features (1hr, 24hr, 168hr) and rolling averages (24hr, 168hr windows)
- **EDA:** Analyzed traffic patterns, correlations, and seasonality with visualizations
- **Modeling:** 
  - Linear Regression (RMSE: 692.57, R²: 0.878)
  - LSTM Neural Network (RMSE: 496.02, R²: 0.937)

**Key Files:**
- `Building_a_Pipeline_for_Time_Series_Data.ipynb` - Full analysis and training notebook
- `LTSM_model.h5` - Trained Keras LSTM model
- `linear_regression_model.pkl` - Trained scikit-learn model

---

### **Task 2: Database Design & Implementation**
**Lead:** Nziza Aime Pacifique

Dual-database architecture for flexible data access:

#### **MySQL (Normalized Schema)**
- **4 Tables:** `traffic`, `datetime_info`, `holiday_info`, `weather_info`
- **ERD:** Available in `Task 2_ databases_updated/mysql/ERD_diagram.md`
- **Benefits:** Data integrity, efficient joins, normalized structure

#### **MongoDB (Denormalized Schema)**
- **Single Collection:** `traffic_data` with all features embedded
- **Index:** Created on `date_time` for fast queries
- **Benefits:** Fast reads, flexible schema, JSON-friendly

**Setup:**
```bash
# MySQL
mysql -u root -p < Task\ 2_\ databases_updated/mysql/mysql_schema.sql
python Task\ 2_\ databases_updated/mysql/clean_data_load.py

# MongoDB
python Task\ 2_\ databases_updated/mongodb/mongo_schema.py
```

**Sample Queries:**
- Full dataset retrieval with joins
- Date range filtering
- Latest record queries

---

### **Task 3: RESTful API Development**
**Lead:** Kayonga Elvis

FastAPI service providing unified access to both databases:

#### **Endpoints**

**MySQL Routes** (`/mysql`):
- `GET /all` - Retrieve all records with joins
- `GET /latest` - Get most recent record
- `GET /single?date_time=YYYY-MM-DD%20HH:MM:SS` - Single record by datetime
- `GET /range?start=...&end=...` - Records in date range
- `GET /last24?date_time=...` - Last 24 records for LSTM input
- `POST /`, `PUT /{id}`, `DELETE /{id}` - CRUD operations

**MongoDB Routes** (`/mongo`):
- `GET /latest` - Most recent document
- `GET /single?date_time=ISO` - Single document by datetime
- `GET /last24?date_time=ISO` - Last 24 documents
- `GET /range?start=...&end=...` - Range query
- `POST /`, `PUT /`, `DELETE /` - CRUD operations

**Start API Server:**
```bash
cd Task\ 3_\ API_updated
pip install -r requirements.txt
uvicorn main:app --reload
```

Access API docs at: `http://127.0.0.1:8000/docs`

---

### **Task 4: Prediction & Inference Pipeline**
**Lead:** Kevin Mike Chris Ntwari

End-to-end prediction workflow integrating API and trained models:

#### **Traditional ML Prediction** (`ml_main.py`, `ml_script1.py`)
1. Fetches single record via `/mysql/single` or `/mongo/single`
2. Preprocesses data (one-hot encoding, feature alignment)
3. Loads `linear_regression_model.pkl`
4. Generates prediction with RMSE evaluation

#### **Deep Learning Prediction** (`dl_main.py`)
1. Fetches 24 sequential records via `/last24` endpoint
2. Reshapes data into LSTM sequence format (1, 24, features)
3. Loads `LTSM_model.h5` and scalers
4. Predicts traffic volume with R² and RMSE metrics

**Run Predictions:**
```bash
# Ensure API is running first (Task 3)
cd Task\ 4_\ Predictions

# Traditional ML
python ml_main.py

# Deep Learning (LSTM)
python dl_main.py
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Data Processing** | Pandas, NumPy |
| **Databases** | MySQL 8.0+, MongoDB 4.0+ |
| **Database Drivers** | SQLAlchemy, PyMySQL, PyMongo |
| **API Framework** | FastAPI, Uvicorn, Pydantic |
| **Machine Learning** | scikit-learn (Linear Regression) |
| **Deep Learning** | TensorFlow 2.14, Keras |
| **Model Serialization** | joblib (.pkl), Keras (.h5) |
| **Data Source** | Kaggle (kagglehub API) |
| **Configuration** | python-dotenv |

---

## ⚙️ Setup Instructions

### **Prerequisites**
- Python 3.9+
- MySQL 8.0+
- MongoDB 4.0+
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/NzizaPacifique250/dataset_db_for_ml.git
cd dataset_db_for_ml
```

### **2. Environment Setup**
Create a `.env` file in the project root:
```env
# MySQL Configuration
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=traffic_db

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=traffic_db
```

### **3. Install Dependencies**
```bash
pip install -r Task\ 3_\ API_updated/requirements.txt
```

### **4. Database Setup** (Task 2)
```bash
# Create MySQL schema
mysql -u root -p < Task\ 2_\ databases_updated/mysql/mysql_schema.sql

# Load data into MySQL
python Task\ 2_\ databases_updated/mysql/clean_data_load.py

# Load data into MongoDB
python Task\ 2_\ databases_updated/mongodb/mongo_schema.py
```

### **5. Start API Server** (Task 3)
```bash
cd Task\ 3_\ API_updated
uvicorn main:app --reload
```

### **6. Run Predictions** (Task 4)
```bash
cd Task\ 4_\ Predictions
python ml_main.py    # Traditional ML
python dl_main.py    # LSTM
```

---

## 📈 Model Performance

| Model | RMSE | R² Score | Notes |
|-------|------|----------|-------|
| Linear Regression | 692.57 | 0.878 | Fast inference, simpler baseline |
| LSTM Neural Network | 496.02 | 0.937 | Better accuracy, requires 24-hour sequence |

---

## 🔍 Key Features

✅ **Complete ML Pipeline:** From raw data to deployed predictions  
✅ **Dual Database Support:** Normalized (MySQL) and denormalized (MongoDB) designs  
✅ **RESTful API:** FastAPI with automatic documentation  
✅ **Time-Series Engineering:** Lag features, rolling averages, temporal decomposition  
✅ **Production-Ready:** Modular code, error handling, environment configuration  
✅ **Reproducible:** Clear setup instructions and version-controlled dependencies  

---

## 📝 Documentation

- **Task 1:** See `Task 1_  EDA and model training/USER_GUIDE.md`
- **Task 2:** See `Task 2_ databases_updated/mysql/ERD_diagram.md`
- **Task 3:** See `Task 3_ API_updated/README.md` and API docs at `/docs`
- **Task 4:** See `Task 4_ Predictions/USER_GUIDE.md`

---

## 🤝 Usage Example

```python
import requests

# Fetch latest traffic data
response = requests.get("http://127.0.0.1:8000/mysql/latest")
data = response.json()

# Get date range
response = requests.get(
    "http://127.0.0.1:8000/mysql/range",
    params={"start": "2018-09-01", "end": "2018-09-07"}
)
records = response.json()

# Predict traffic for specific datetime
import joblib
import pandas as pd

model = joblib.load("Task 4_ Predictions/linear_regression_model.pkl")
# ... preprocess data ...
prediction = model.predict(X)
```

---

## 📄 License

This project is part of an academic assignment for demonstrating time-series analysis, database design, and API development skills.

---

## 🙏 Acknowledgments

- **Dataset:** [Metro Interstate Traffic Volume](https://www.kaggle.com/datasets/mikedev/metro-traffic-volume) by Mike Dev on Kaggle
- **Institution:** Academic group project (4-member team)
- **Technologies:** Built with open-source tools and frameworks

---

## 📧 Contact

For questions or collaboration:
- **Repository:** [github.com/NzizaPacifique250/dataset_db_for_ml](https://github.com/NzizaPacifique250/dataset_db_for_ml)
- **Contributors:** Emmanuella Asoliya Briggs, Nziza Aime Pacifique, Kayonga Elvis, Kevin Mike Chris Ntwari
