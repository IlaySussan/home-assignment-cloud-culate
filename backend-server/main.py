from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

from utils.architecture_parser import AIArchitectureParser
from utils.types import ScrapeRequest, ArchitectureOut

ai_parser: AIArchitectureParser = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes global dependencies (AI parser, MongoDB connection) when the FastAPI app starts,
    and gracefully closes them on shutdown.
    """
    global ai_parser
    ai_parser = AIArchitectureParser(
        gemini_api_key=os.getenv("GEMINI_API_KEY", "your-gemini-api-key"),
        mongo_uri=os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
        db_name=os.getenv("MONGO_DB_NAME", "aws_architectures"),
        collection_name=os.getenv("MONGO_DB_COLLECTION", "architectures"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    )
    yield
    if ai_parser:
        ai_parser.mongo_client.close()


app = FastAPI(
    title="AWS Architecture AI Scraper",
    description="API for scraping and parsing AWS cloud architectures using AI",
    lifespan=lifespan
)

# Enable CORS for all origins (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", summary="Health Check", response_description="Service status")
@app.get("/", include_in_schema=False)
async def health():
    """
    Health check endpoint. Returns a simple message indicating the API is running.
    """
    return {"status": "AWS Architecture Scraper API service is up and running"}


@app.post("/scrape", summary="Scrape and parse AWS architecture", status_code=HTTPStatus.CREATED)
async def trigger_scraping(request: ScrapeRequest):
    """
    Triggers scraping and AI-based parsing of the given AWS architecture URL.

    Parameters:
        request (ScrapeRequest): JSON payload containing the URL to scrape.

    Returns:
        JSON message confirming scraping success or HTTP 500 error.
    """
    try:
        await ai_parser.scrape_single_url(request.url)
        return JSONResponse(content={"message": f"Scraped {request.url} successfully"}, status_code=HTTPStatus.CREATED)

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Failed to scrape url: {request.url}, Error: {str(e)}")


@app.get("/architectures", response_model=List[ArchitectureOut], summary="Get all parsed architectures")
async def get_all_architectures():
    """
    Retrieves all architectures stored in the database.

    Returns:
        List of architecture documents.
    """
    try:
        architectures = await ai_parser.get_all_architectures()
        return architectures
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Failed to retrieve architectures: {str(e)}")


@app.delete("/architectures", summary="Delete all architectures")
async def clear_all_architectures():
    """
    Deletes all architecture entries from the database (for testing or cleanup).

    Returns:
        JSON message with number of documents deleted.
    """
    try:
        result = await ai_parser.mongo_client.delete_all()
        return {"message": f"Deleted {result.deleted_count} architectures"}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Failed to clear architectures: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
