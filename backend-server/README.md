# 👀 AWS Architecture Scraper with AI (Gemini + FastAPI + MongoDB)

This project is a backend service that scrapes AWS architecture documentation pages and uses **Gemini AI** to intelligently extract structured data like services, components, use cases, and benefits.

---

## 🚀 Features

* ✅ Scrapes AWS architecture pages using `aiohttp` and `BeautifulSoup`
* ✅ Uses **Google Gemini AI** to extract structured architecture information
* ✅ Stores parsed data in **MongoDB**
* ✅ Provides a **FastAPI** interface to trigger scraping and fetch stored data
* ✅ Classifies result status: `Success`, `Partial`, or `Failed`
* ✅ Fully asynchronous (FastAPI + `motor`)
* ✅ Logs with levels and environment control

---

## 📁 Project Structure

```bash
.
├── app/
│   ├── main.py                # FastAPI application
│   └── utils/
│       ├── ai_parser.py       # AI architecture parser
│       ├── mongo_client.py    # Async MongoDB handler (motor)
│       ├── logger_service.py  # Logger setup
│       └── types.py           # Pydantic models & Enums
├── .env.example               # Environment variable template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone & install dependencies

```bash
git clone <your-repo>
cd <your-repo>
pip install -r requirements.txt
```

### 2. Create `.env` file

```bash
cp .env.example .env
```

And fill it with your keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=architectures
MONGO_DB_COLLECTION=aws_architectures
```

---

## ▶️ Running the API

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Example usage

### Trigger scrape

```http
POST /scrape
Content-Type: application/json

{
  "url": "https://aws.amazon.com/solutions/implementations/serverless-image-handler/"
}
```

### Get all parsed architectures

```http
GET /architectures
```

### Delete all (for testing)

```http
DELETE /architectures
```

### Health check

```http
GET /
```

---

## 📄 Sample AI Output

```json
{
  "title": "Serverless Image Handler",
  "description": "Resizes and optimizes images on the fly using Lambda@Edge, S3, and CloudFront.",
  "services": ["Lambda", "S3", "CloudFront", "CloudWatch"],
  "components": [
    {
      "name": "Lambda@Edge",
      "type": "aws_service",
      "description": "Processes and resizes images on the fly."
    }
  ],
  "use_case": "Optimized content delivery for web/mobile applications",
  "complexity": "Medium",
  "estimated_cost": "Depends on traffic and usage",
  "benefits": [
    "On-the-fly image transformation",
    "Reduced storage and latency",
    "Scalable and serverless"
  ],
  "architecture_pattern": "Serverless",
  "source_url": "...",
  "scraped_at": "2025-07-11T19:03:34Z",
  "raw_title": "...",
  "parsing_status": "Success"
}
```

---

## 📊 Parsing Status

Each result is classified based on quality:

| Status    | Meaning                                       |
| --------- | --------------------------------------------- |
| `Success` | Full AI parse with real AWS services          |
| `Failed`  | AI failed, fallback was used                  |

---

## 📦 Logging

Logging is configured via `.env` using the `LOG_LEVEL` variable. All logs go to `stdout` for Docker/Kubernetes compatibility.

---

## 🧐 Technologies Used

* [FastAPI](https://fastapi.tiangolo.com/)
* [Motor](https://motor.readthedocs.io/) (async MongoDB)
* [Google Generative AI](https://ai.google.dev/)
* [aiohttp](https://docs.aiohttp.org/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [Pydantic](https://docs.pydantic.dev/)


