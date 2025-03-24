# Trading Strategy API
This project is a FastAPI-based application that implements a simple Moving Average Crossover Strategy. It fetches historical ticker data from a PostgreSQL database, calculates short-term and long-term moving averages, generates buy/sell/hold signals, and computes performance metrics such as the cumulative return. The application exposes both JSON endpoints and HTML pages for viewing results.


![Screenshot](Screenshots/Image1.png)
![Screenshot](Screenshots/Image2.png)
![Screenshot](Screenshots/Image3.png)
![Screenshot](Screenshots/Image4.png)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Locally (Uvicorn)](#running-locally)
  - [Using Docker](#running-with-docker)
- [Endpoints](#endpoints)
- [Seeding Data](#seeding-data)
- [License](#license)

## Features

- **Database Integration:** Stores ticker data (datetime, open, high, low, close, volume, instrument) in PostgreSQL.
- **CRUD Endpoints:** Create and retrieve ticker data.
- **Trading Strategy:** Implements a moving average crossover strategy to generate buy/sell/hold signals.
- **Performance Metrics:** Calculates cumulative return and signal counts.
- **Web Interface:** Renders strategy performance and dataset in a browser using Jinja2 templates.
- **Dockerized:** Containerized using Docker for easy deployment.

## Project Structure

```
trading_project/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application with endpoints
│   ├── models.py         # Pydantic models for data validation
│   ├── database.py       # Database connection logic
│   ├── crud.py           # CRUD operations for ticker data
│   └── strategy.py       # Trading strategy calculations
├── templates/
│   └── strategy.html     # Jinja2 template for displaying strategy results and dataset
├── Screenshots/
│   └── Image1.png        # Project screenshot
├── requirements.txt      # Project dependencies
├── Dockerfile            # Docker configuration for containerizing the app
└── README.md             # Project documentation (this file)
```

## Prerequisites

- **Python 3.8+**
- **PostgreSQL**: Install from [postgresql.org/download](https://www.postgresql.org/download/)
- **Docker Desktop** (optional): For containerizing the application
- **Node.js** (if using additional tooling)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/trading_project.git
   cd trading_project
   ```

2. **Set Up Virtual Environment and Install Dependencies:**

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` File:**  
   In the project root, create a file named `.env` (make sure it is not tracked by Git if it contains sensitive credentials).

2. **Add Your PostgreSQL Connection String:**  
   In the `.env` file, add the following line, replacing the placeholders with your actual credentials:

   ```ini
   DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/trading_db"
   ```

   This connection string is used by the application (in `app/database.py`) to connect to your PostgreSQL database.

## Running the Application

### Running Locally

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to:

- **Root:** [http://localhost:8000](http://localhost:8000)
- **JSON Strategy Performance:** [http://localhost:8000/strategy/performance](http://localhost:8000/strategy/performance)
- **HTML Strategy Performance:** [http://localhost:8000/strategy/performance/html](http://localhost:8000/strategy/performance/html)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Running with Docker

1. **Build the Docker Image:**

   ```bash
   docker build -t trading_app .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -d -p 8000:8000 trading_app
   ```

3. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Endpoints

- **GET /**  
  Returns a welcome message.

- **GET /data**  
  Returns all ticker data in JSON format.

- **POST /data**  
  Inserts new ticker data into the database.  
  **Example Request Body:**
  ```json
  {
    "datetime": "2025-03-20T09:45:00",
    "open": 100.75,
    "high": 101.25,
    "low": 100.50,
    "close": 101.00,
    "volume": 2000,
    "instrument": "ExampleInstrument"
  }
  ```

- **GET /strategy/performance**  
  Returns JSON with strategy performance metrics (cumulative return, buy/sell/hold signal counts).

- **GET /strategy/performance/html**  
  Renders an HTML page that shows:
  - Cumulative return
  - Signal counts (buy, sell, hold)
  - The full dataset with computed signals

## Seeding Data

If you have a CSV or a Google Sheets dataset, create a seed script (e.g., `seed.py`) to load the data into your database.
