from ninja import FilterSchema, Schema
from pydantic import PositiveInt
from enum import StrEnum


class SearchEntityType(StrEnum):
    artist = "artist"
    release = "release"
    track = "track"


class SearchOutSchema(Schema):
    entity_id: PositiveInt
    name: str
    entity: SearchEntityType
    score: float
