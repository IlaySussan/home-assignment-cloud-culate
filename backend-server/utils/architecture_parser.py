import asyncio
import os
import uuid

import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import json
import google.generativeai as genai
from datetime import datetime
from uuid import uuid4

from .logger_service import get_logger
from .mongo_client import MongoHandler
from .types import ParsingStatusEnum

logger = get_logger(__name__)


class AIArchitectureParser:
    def __init__(self, gemini_api_key: str, mongo_uri: str, db_name: str, collection_name: str, gemini_model: str):
        """
        Initialize the AIArchitectureParser with Gemini API and MongoDB connection.

        Args:
            gemini_api_key (str): API key for Google Gemini.
            mongo_uri (str): URI for MongoDB.
            db_name (str): Name of the MongoDB database.
            collection_name (str): Name of the MongoDB collection.
        """
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(gemini_model)
        self.mongo_client = MongoHandler(mongo_uri, db_name, collection_name)
        logger.info("AIArchitectureParser initialized with Gemini and MongoDB")

    async def scrape_single_url(self, url: str) -> Optional[Dict]:
        """
        Scrapes a single AWS architecture page and parses it using AI.

        Args:
            url (str): The URL of the AWS architecture page.

        Returns:
            Optional[Dict]: Parsed architecture data, or None on failure.
        """
        logger.info(f"Starting scrape for URL: {url}")
        try:
            async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(int(os.getenv("REQUESTS_TIMEOUT", '30')))) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        logger.info(f"Successfully fetched content from: {url}")
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        raw_content = {
                            'title': soup.find('title').text if soup.find('title') else '',
                            'content': soup.get_text(),
                            'url': url,
                            'scraped_at': datetime.now()
                        }

                        parsed_data = await asyncio.to_thread(self._ai_parse_content, raw_content)

                        await self.store_architecture(parsed_data)
                        logger.info(f"Finished parsing and storing architecture from: {url}")
                        return parsed_data
                    else:
                        logger.warning(f"Received non-200 response ({response.status}) for URL: {url}")

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
        return None

    def _ai_parse_content(self, raw_content: Dict) -> Dict:
        """
        Uses Gemini AI to parse AWS architecture content and extract structured information.

        Args:
            raw_content (Dict): Dictionary with raw HTML content and metadata.

        Returns:
            Dict: Parsed structured architecture data.
        """
        logger.info(f"Parsing content with Gemini for: {raw_content['url']}")

        prompt = f"""
        Analyze the following AWS architecture content and extract structured information:

        Title: {raw_content['title']}
        Content: {raw_content['content'][:3000]}...

        Please extract and return JSON with the following structure:
        {{
            "title": "Clean architecture title",
            "description": "Brief description of the architecture",
            "services": ["list", "of", "aws", "services", "mentioned"],
            "components": [
                {{"name": "component_name", "type": "aws_service", "description": "what it does"}}
            ],
            "use_case": "Primary use case or industry",
            "complexity": "Simple/Medium/Complex",
            "estimated_cost": "Cost estimation if mentioned",
            "benefits": ["key", "benefits", "listed"],
            "architecture_pattern": "Pattern type (e.g., microservices, serverless, etc.)"
        }}

        Focus on:
        - AWS services mentioned (EC2, S3, Lambda, RDS, etc.)
        - Architecture components and their relationships
        - Use cases and benefits
        - Cost considerations
        - Scalability and performance aspects
        """
        try:
            response = self.model.generate_content(prompt)
            ai_response = response.text.strip()

            if ai_response.startswith('```json'):
                ai_response = ai_response[7:-3]
            elif ai_response.startswith('```'):
                ai_response = ai_response[3:-3]

            try:
                parsed_json = json.loads(ai_response)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                if json_match:
                    parsed_json = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse AI response as JSON")

            parsed_json.update({
                'source_url': raw_content['url'],
                'scraped_at': raw_content['scraped_at'],
                'raw_title': raw_content['title'],
                "parsing_status": ParsingStatusEnum.Success.value,
                "id": str(uuid4())
            })

            logger.info(f"Successfully parsed architecture from: {raw_content['url']}")
            return parsed_json

        except Exception as e:
            logger.error(f"Gemini parsing error for {raw_content['url']}: {str(e)}")
            return self._fallback_parse(raw_content)

    def _fallback_parse(self, raw_content: Dict) -> Dict:
        """
        Fallback parsing logic when AI-based parsing fails.

        Args:
            raw_content (Dict): Raw HTML content and metadata.

        Returns:
            Dict: Minimal architecture data with fallback flag.
        """
        logger.warning(f"Using fallback parser for: {raw_content['url']}")
        return {
            'title': raw_content['title'],
            'description': 'Failed to parse with AI',
            'services': [],
            'components': [],
            'use_case': 'Unknown',
            'complexity': 'Unknown',
            'benefits': [],
            'source_url': raw_content['url'],
            'scraped_at': raw_content['scraped_at'],
            'parsing_status': ParsingStatusEnum.Failed.value,
            "id": str(uuid4())
        }

    async def store_architecture(self, architecture_data: Dict) -> str:
        """
        Store parsed architecture in MongoDB.

        Args:
            architecture_data (Dict): The parsed architecture document.

        Returns:
            str: The ID of the inserted document.
        """
        try:
            result = await self.mongo_client.insert(architecture_data)
            logger.info(f"Stored architecture: {architecture_data.get('title', 'Unknown')}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error storing architecture: {str(e)}")
            raise

    async def get_all_architectures(self) -> List[Dict]:
        """
        Retrieves all stored architectures from MongoDB.

        Returns:
            List[Dict]: List of architecture documents.
        """
        try:
            logger.info("Retrieving all stored architectures from MongoDB")
            return await self.mongo_client.get_all()
        except Exception as e:
            logger.error(f"Error retrieving architectures: {str(e)}")
            return []
