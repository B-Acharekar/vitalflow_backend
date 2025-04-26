
# VitalFlow Backend

VitalFlow is a health monitoring system that integrates health data from Android devices using Flutter and Kotlin, processes it through a Flask-based backend, and stores insights in a MongoDB database. This backend handles API endpoints for health metrics like steps, heart rate, sleep, hydration, stress levels, and daily performance.

---

## Features

- User Authentication (Signup/Login with bcrypt password hashing)
- Health Data Syncing from Health Connect (Steps, Heart Rate, Sleep, etc.)
- Water Intake Logging (Manual and estimated via NLP)
- Stress Detection (Text-based and calculated from vitals)
- Sleep Monitoring using bedtime schedule
- Performance & Insights Engine combining metrics
- Data Visualization Support for graphs and trends (via API)

---

## Tech Stack

| Layer       | Tech                         |
|-------------|------------------------------|
| Backend     | Python, Flask                |
| Database    | MongoDB                      |
| Auth        | Bcrypt, JWT (optional)       |
| API Design  | RESTful                      |
| NLP Model   | Scikit-learn / SpaCy / Custom ML |
| Platform    | Android (Flutter & Kotlin)   |

---

## Project Structure

```
vitalflow_backend/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── health_data.py
│   │   ├── water_log.py
│   │   ├── stress_log.py
│   │   └── insights.py
│   ├── models/
│   │   ├── user.py
│   │   ├── health.py
│   │   └── utils.py
│   └── nlp/
│       ├── water_parser.py
│       └── stress_analyzer.py
│
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/B-Acharekar/vitalflow_backend.git
cd vitalflow_backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```
MONGO_URI=mongodb://localhost:27017/vitalflow
SECRET_KEY=your-secret-key
```

### 5. Run the Server

```bash
python run.py
```

Server runs at `http://localhost:5000/`

---

## API Endpoints Overview

| Method | Endpoint               | Description                      |
|--------|------------------------|----------------------------------|
| POST   | `/signup`              | Register a new user              |
| POST   | `/login`               | Authenticate user                |
| POST   | `/health/steps`        | Log step data                    |
| POST   | `/health/heart-rate`   | Log heart rate                   |
| POST   | `/health/sleep`        | Log sleep duration               |
| POST   | `/water/log`           | Log water intake                 |
| POST   | `/stress/analyze`      | Log and analyze stress input     |
| GET    | `/insights/day`        | Get daily performance insights   |

---

## NLP and Stress Estimation

- **Water Intake Parsing**: Converts phrases like "drank a glass of water" into estimated ml values.
- **Stress Detection**: Based on sentiment analysis or derived from heart rate and sleep data.

---

## Future Improvements

- Add unit and integration tests
- Add Swagger/OpenAPI documentation
- Dockerize for containerized deployment
- Implement CI/CD pipeline
```
