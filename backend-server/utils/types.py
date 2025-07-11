from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ParsingStatusEnum(Enum):
    Success = "Success"
    Failed = "Failed"


class Component(BaseModel):
    name: str
    type: str
    description: str


class ArchitectureOut(BaseModel):
    title: Optional[str] = None
    description: Optional[str]
    services: List[str]
    components: List[Component]
    use_case: Optional[str] = None
    complexity: Optional[str]
    estimated_cost: Optional[str] = None
    benefits: List[str]
    architecture_pattern: Optional[str] = None
    source_url: str
    scraped_at: datetime
    raw_title: Optional[str] = None
    parsing_status: ParsingStatusEnum
