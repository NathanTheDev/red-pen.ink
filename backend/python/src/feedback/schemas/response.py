from pydantic import BaseModel


class Annotation(BaseModel):
    span: str
    comment: str


class CheckResponse(BaseModel):
    content: str
    annotations: list[Annotation]
