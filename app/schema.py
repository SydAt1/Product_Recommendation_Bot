from pydantic import BaseModel

# Description Schema
class DescriptionInput(BaseModel):
    description: str