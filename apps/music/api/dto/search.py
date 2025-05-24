from enum import StrEnum

from ninja import Schema
from pydantic import PositiveInt


class SearchEntityType(StrEnum):
    artist = "artist"
    release = "release"
    track = "track"


class SearchOutSchema(Schema):
    entity_id: PositiveInt
    name: str
    entity: SearchEntityType
    score: float
