from pydantic import BaseModel
from uuid import uuid4

class Task(BaseModel):
    id: str = ""
    title: str
    done: bool = False

    def __init__(self, **data):
        if not data.get("id"):
            data["id"] = str(uuid4())[:8]
        super().__init__(**data)
