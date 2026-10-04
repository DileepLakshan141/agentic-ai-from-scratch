from pydantic import BaseModel
from typing import List, Optional


class UserProfile(BaseModel):
    name: str
    age: int
    skills: List[str]
    email: Optional[str] = None

raw_json = '{"name": "John Doe", "age": 30, "skills": ["Python", "FastAPI"], "email": "john.doe@example.com"}'

user = UserProfile.model_validate_json(raw_json)

print(user.name)
print(user.skills)
