from pydantic import BaseModel
import json

class Todo(BaseModel):
    title: str
    completed: bool = False

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
        }
    def to_json(self):
        return json.dumps(self.to_dict())