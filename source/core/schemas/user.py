from pydantic import BaseModel

from typing import Optional
from datetime import datetime

class UserDTO(BaseModel):
    id: int
    username: Optional[str] = ""
    created_at: Optional[datetime] = None