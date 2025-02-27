from dataclasses import dataclass
from datetime import datetime


@dataclass
class Story:
    source: str
    title: str
    summary: str
    retrieved: datetime
    datetime: datetime
