from typing import Optional

class Connection:
    id: str
    personId: str
    date: str # TODO date might not be a string

class Person:
    id: str
    name: Optional[str]
    type: str
    frequencyDays: int

class User:
    id: str
    email: str
    firstName: str
    lastName: str
