# Task 2: Databases

This directory contains the database design and implementation for the Metro Interstate Traffic Volume dataset. The goal of this task is to set up the data storage layer for the machine learning pipeline, allowing us to manage and query the raw data before preprocessing and model training.

To evaluate different storage strategies, the data modeling has been implemented using two different database paradigms: a relational database (SQL) and a document-based database (MongoDB).

## Directory Structure

The repository is organized into the following folders:

* `sql/`: Contains the relational database implementation.
* `mongodb/`: Contains the NoSQL document database implementation.
* `assets/`: Contains supporting files or diagrams relating to the database design.

## SQL Implementation

The relational approach uses a normalized schema to minimize data redundancy and enforce data integrity. The design consists of a central fact table for traffic observations and separate dimension tables for holidays and weather conditions.

Files provided:
* `schema.sql`: Contains the DDL statements to set up the `traffic_db` database and create the `holidays`, `weather_conditions`, and `traffic_records` tables with their respective foreign key relationships.
* `load_data.sql`: Statements and scripts for inserting the initial dataset into the SQL database.
* `queries.sql`: A collection of sample SQL queries to extract and analyze data (e.g., finding traffic volume during specific weather conditions).

## MongoDB Implementation

The NoSQL approach uses a denormalized document structure. Instead of splitting data across multiple tables, related attributes—such as weather conditions—are embedded directly within each traffic record document. This allows for faster read operations when retrieving complete records for the model.

Files provided:
* `collection_design.js`: Outlines the JSON schema validation and structure for the `traffic_data` collection.
* `load_sample_data.py`: A Python script that uses `pymongo` to connect to a local MongoDB instance, create the collection, build necessary indexes (like date and weather), and load sample documents.
* `queries.js`: Sample MongoDB find operations and aggregation pipelines for analyzing the dataset.

## Execution

For the SQL implementation, execute the scripts sequentially (`schema.sql` -> `load_data.sql` -> `queries.sql`) using your preferred SQL client.

For the MongoDB implementation, ensure you have a local instance running on the default port (27017). Install `pymongo`, then run the `load_sample_data.py` script to generate the database and populate the records.
