from .base import BaseSchema


class RootResponseSchema(BaseSchema):
    project: str
    summary: str
    version: str
    status: str
    timestamp: str


class HealthComponentsSchema(BaseSchema):
    store: str
    database: str


class HealthResponseSchema(BaseSchema):
    status: str
    components: HealthComponentsSchema
