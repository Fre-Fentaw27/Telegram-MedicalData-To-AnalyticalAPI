# Telegram-MedicalData-To-AnalyticalAPI

An end-to-end data pipeline for Telegram, leveraging dbt for transformation, Dagster for orchestration, and YOLOv8 for data enrichment.

# Task 0: Project Setup & Environment Management

## 📦 Prerequisites

- Python 3.8+
- PostgreSQL 13+
- pgAdmin 4
- Git

## 🛠️ Setup Instructions

## Clone the repository

- git clone https://github.com/yourusername/Telegram-MedicalData-To-AnalyticalAPI.git
- cd Telegram-MedicalData-To-AnalyticalAPI

## Create and activate virtual environment

- python -m venv .venv
- source .venv/bin/activate # Linux/Mac
- .\.venv\Scripts\activate # Windows

## Install Python dependencies

- pip install -r requirements.txt

- Set up PostgreSQL

- Configure environment variables (.env file)

# Task 1: Data Scraping and Collection (Extract & Load)

### 📋 Data Sources

Telegram channels:

- @CheMed123
- @lobelia4cosmetics
- @tikvahpharma

## 📂 Project Structure

data/
├── raw/ # Raw JSON files
│ └── telegram_messages/
│ ├── 2022-09-05/
│ │ └── CheMed123.json
│ └── 2025-05-20/
│ └── lobelia4cosmetics.json
└── processed/ # Cleaned data
src/
├── scraping/
│ ├── telegram_scraper.py
│ └── data_loader.py
└── load_to_postgres.py

## 🔧 Key Components

- Telegram Scraper (telegram_scraper.py)

## 🚀 Execution Flow

## Run the scraper (saves to JSON)

- python src/scraping/telegram_scraper.py

## 📊 Sample Output

Loaded 76 messages from data/raw/telegram_messages/2022-09-05/CheMed123.json
Loaded 1000 messages from data/raw/telegram_messages/2025-05-20/lobelia4cosmetics.json

# Task 2: Data Modeling and Transformation (Transform)

# Medical Analytics Data Transformation (dbt Project)

## 📌 Project Overview

This dbt project transforms raw Telegram medical channel messages from JSON files into an analytics-ready star schema in PostgreSQL. It serves as the "data transformation" layer between raw data and analytics/BI tools.

## 🛠️ Technical Stack

- **Database**: PostgreSQL
- **Transformation**: dbt (data build tool)
- **Data Sources**: JSON files scraped from Telegram channels
- **Schemas**:
  - `raw`: Original ingested data
  - `staging`: Cleaned source data
  - `analytics`: Dimensional model

## 📂 Project Structure

medical_analytics/
├── dbt_project.yml # Project configuration
├── models/
│ ├── staging/ # Staging models
│ │ ├── stg_telegram_messages.sql
│ │ └── schema.yml # Tests & docs
│ └── marts/
│ ├── core/ # Dimensional models
│ │ ├── dim_channels.sql
│ │ ├── dim_dates.sql
│ │ ├── fct_messages.sql
│ └── schema.yml
├── tests/
│ └── custom_data_tests/ # Custom data quality tests
├── macros/ # Reusable SQL code
└── packages.yml # dbt dependencies

## 🔄 Data Flow

1. **Raw Data**: JSON files → `raw.telegram_messages`
2. **Staging**:
   - Cleans raw data
   - Standardizes fields
   - Light transformations
   - Output: `staging.stg_telegram_messages`
3. **Marts**:
   - `dim_channels`: Channel metadata
   - `dim_dates`: Time dimensions
   - `fct_messages`: Message facts with foreign keys

## 🧪 Data Quality Tests

## Custom Tests

🚀 How to Run
Install dependencies:

- dbt deps
  Run transformations:
- dbt run
  Run tests:
- dbt test
  Generate docs:
- dbt docs generate
- dbt docs serve

## 🛠️ Common Operations

Command Description

- dbt run --select staging(Run only staging models)
- dbt test --select stg_telegram_messages (Test only staging)
- dbt run --exclude dim_dates (Run all except dim_dates)

## Data Flow Diagram

![Data Transformation Flow](images/image.png)

## 🧪 Data Quality Tests

### Automated Tests

```yaml
# Example from schema.yml
columns:
  - name: message_id
    tests:
      - unique
      - not_null
  - name: message_date
    tests:
      - not_null
```

# Task 3: Data Modeling and Transformation (Transform)

# This directory (`models/marts/core`) contains the dbt models related to analyzing object detections within Telegram images. This task focuses on transforming raw image detection results into a usable fact table for further analytical insights.

#

# ## Overview

#

# The primary goal of Task 3 is to provide a clean, reliable, and easily consumable dataset for understanding what objects are being detected in the images shared across Telegram channels. This fact table (`fct_image_detections`) can then be joined with other dimension tables (e.g., `dim_channels`, `dim_dates`) to gain insights into:

#

# \* Most frequently detected objects.

# \* Detection confidence levels.

# \* Objects detected in specific channels or over time.

# \* Correlation between image content and message engagement (future analysis).

#

# ## Data Sources

#

# This task relies on the following upstream data sources:

#

# \* `stg_telegram_messages`: A staging model that cleans and prepares raw Telegram message data, including a flag (`is_image_flag`) to identify image messages and their `image_path`.

# \* `fct_image_detections` (source): The raw, un-transformed object detection results generated by the Python script. This table typically contains `message_id`, `detected_object_class`, and `confidence_score`.

#

# ## Models

#

# ### `fct_image_detections`

#

# \* **Description**: This is a fact table containing each individual object detection result for image messages. It enriches the raw detection data with cleaned message information and calculates a percentage-based confidence score.

# \* **Materialization**: `table` (for performance and explicit snapshotting of detection results).

# \* **Columns**:

# \* `detection_key` (Primary Key, Surrogate Key): A unique identifier for each distinct object detection (combination of `message_id` and `detected_object_class`).

# \* `message_id` (Foreign Key): Links back to the `fct_messages` table to provide context about the original Telegram message.

# \* `detected_object_class`: The class of the object identified by the detection model (e.g., 'person', 'car', 'medical_device').

# \* `confidence_score_pct`: The confidence level of the detection, expressed as a percentage (rounded to two decimal places).

# \* `image_path`: The file path to the image where the object was detected.

# \* **Transformations**:

# \* Joins `stg_telegram_messages` to filter for `is_image_flag = TRUE` messages and retrieve `image_path`.

# \* Calculates `confidence_score_pct` by multiplying `confidence_score` by 100 and rounding to two decimal places.

# \* Generates `detection_key` using `dbt_utils.generate_surrogate_key` for composite uniqueness.

#

# ## Testing Strategy

#

# To ensure data quality and integrity, the following tests are applied:

#

# \* **`fct_image_detections`**:

# \* `detection_key`: `unique`, `not_null`

# \* `message_id`: `not_null`, `relationships` (to `fct_messages.message_id`)

# \* `detected_object_class`: `not_null`

# \* `confidence_score_pct`: `not_null`, custom test for values `BETWEEN 0 AND 100`.

# \* `image_path`: `not_null` (assuming all processed image messages will have a path).

#

# ## Future Enhancements

#

# \* **Granular Object Dimensions**: Create a `dim_objects` table to standardize object classes and potentially add more attributes (e.g., object categories, descriptions).

# \* **Performance Optimization**: Explore partitioning `fct_image_detections` by `message_date` if the table grows very large.

# \* **Error Handling**: Implement more robust error handling or anomaly detection for very low confidence scores or unexpected object classes.

# \* **Data Lineage Visualization**: Leverage dbt's built-in documentation and lineage graphs to better visualize the flow from raw data to this fact table.
