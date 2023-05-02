from typing import Optional
from enum import StrEnum, auto


class RelationshipType(StrEnum):
    FRIEND = (auto(),)
    FAMILY = (auto(),)
    COLLEAGUE = (auto(),)


class Connection:
    id: str
    createdAt: int
    notes: str

    def from_dict(self, input):
        self.id = input.get("id")
        self.createdAt = input.get("createdAt")
        self.notes = input.get("notes")


class Person:
    id: str
    firstName: Optional[str]
    lastName: Optional[str]
    relationshipType: RelationshipType
    frequencyDays: int

    def from_dict(self, input: dict):
        self.id = input.get("id")
        self.relationshipType = input.get("relationshipType")
        self.frequencyDays = input.get("frequencyDays")
        self.firstName = input.get("firstName")
        self.lastName = input.get("lastName")


class User:
    id: str
    email: str
    firstName: str
    lastName: str
    createdAt: int
    updatedAt: Optional[int]

    def from_dict(self, input: dict):
        self.id = input.get("id")
        self.firstName = input.get("firstName")
        self.lastName = input.get("lastName")
        self.email = input.get("email")
        self.createdAt = input.get("createdAt")
        self.updatedAt = input.get("updatedAt")
