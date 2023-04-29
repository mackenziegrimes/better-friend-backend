from typing import Optional


class Connection:
    id: str
    personId: str
    date: str  # TODO date might not be a string


class Person:
    id: str
    name: Optional[str]
    relationshipType: str
    frequencyDays: int


class User:
    id: str
    email: str
    firstName: str
    lastName: str
    createdAt: int
    updatedAt: Optional[int]

    def from_dict(self, input: dict):
        self.id = input["id"]
        self.firstName = input["firstName"]
        self.lastName = input["lastName"]
        self.email = input["email"]
        self.createdAt = input["createdAt"]

        if "updatedAt" in input:
            self.updatedAt = input["updatedAt"]
