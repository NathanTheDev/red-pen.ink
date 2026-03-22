from pydantic import BaseModel


class Annotation(BaseModel):
    span: str
    comment: str
