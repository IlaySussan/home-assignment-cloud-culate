# AWS Cloud Architecture Scraper - Home Assignment

This project is a full-stack system for scraping and parsing AWS architecture solutions using **Google Gemini AI**, built as part of a technical home assignment.

The system includes:

* A **FastAPI backend** to scrape and parse content using Gemini AI
* A **MongoDB database** to persist structured architecture data
* A **Vite + React frontend** to display the parsed data interactively

---

## ⚙️ Setup & Run

### 1. Requirements

* Docker + Docker Compose
* A `.env` file with your Gemini API key and MongoDB settings

### 2. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-dir>
```

### 3. Create a `.env` file

```bash
# .env
GEMINI_API_KEY=your-gemini-api-key-here
MONGO_URI=mongodb://admin:home-assignment-cloud-culate@mongodb:27017/
MONGO_DB_NAME=aws_architectures
MONGO_DB_COLLECTION=architectures
VITE_BACKEND_API_URL=http://localhost:8000
REQUESTS_TIMEOUT=30
GEMINI_MODEL=gemini-2.5-pro
```

### 4. Start the stack

```bash
docker compose --env-file .env up
```

---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── .env
├── backend-server/        # FastAPI backend
│   └── main.py, app code...
├── frontend/              # React + Vite frontend
│   └── App.tsx, etc.
```

---

## 🚀 Services (from docker-compose)

### `mongodb`

* MongoDB container
* Stores all parsed AWS architectures
* No exposed ports (internal access only)

### `backend`

* FastAPI app served via Uvicorn
* Connects to Gemini and MongoDB
* Exposed at: [http://localhost:8000](http://localhost:8000)
* Environment variables:

  * `GEMINI_API_KEY` – Your API key
  * `MONGO_URI` – MongoDB connection URI
  * `MONGO_DB_NAME` – Name of the database
  * `MONGO_DB_COLLECTION` – Name of the collection
  * `GEMINI_MODEL` – Gemini model to use (default: gemini-2.5-pro)
  * `REQUESTS_TIMEOUT` – Timeout for HTTP requests (default: 30 seconds)

### `frontend`

* Vite + React app
* Exposed at: [http://localhost:5173](http://localhost:5173)
* Talks to backend via `VITE_BACKEND_API_URL=http://localhost:8000`

---

## 🧠 How to get your Gemini API key

1. Go to [Google AI Studio](https://makersuite.google.com/app)
2. Sign in with your Google account
3. Click on **API key** in the top right corner
4. Click **Create API key**
5. Copy the key and paste it into your `.env` file under `GEMINI_API_KEY`

🔐 Note: Gemini API access may be limited by region or project type (e.g., personal, enterprise).

---

## 🔌 API Endpoints

| Method | Path             | Description                         |
| ------ | ---------------- | ----------------------------------- |
| GET    | `/` or `/health` | Health check                        |
| POST   | `/scrape`        | Scrape and parse AWS architecture   |
| GET    | `/architectures` | Get all stored parsed architectures |
| DELETE | `/architectures` | Delete all stored architectures     |

---

## 📄 Example `.env`

```env
# Google Gemini API Key
GEMINI_API_KEY=your_api_key

# MongoDB connection
MONGO_URI=mongodb://admin:home-assignment-cloud-culate@mongodb:27017/
MONGO_DB_NAME=aws_architectures
MONGO_DB_COLLECTION=architectures

# Logging and runtime configuration
REQUESTS_TIMEOUT=30
GEMINI_MODEL=gemini-2.5-pro

# React frontend environment
VITE_BACKEND_API_URL=http://localhost:8000
```

---

## 🧠 Technologies

* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
* [Motor (async Mongo)](https://motor.readthedocs.io/)
* [Google Generative AI (Gemini)](https://ai.google.dev/)
* [Docker Compose](https://docs.docker.com/compose/)
* [React + Vite](https://vitejs.dev/)

