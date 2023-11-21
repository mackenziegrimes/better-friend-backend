"""Dataclasses of DB models"""
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional, Self


class RelationshipType(StrEnum):
    """Enum for possible relationship types of a Person"""
    FRIEND = (auto(),)
    FAMILY = (auto(),)
    COLLEAGUE = (auto(),)


@dataclass
class Connection:
    """Dataclass for Connection db object"""
    id: str
    createdAt: int
    notes: str = ''

    @classmethod
    def from_dict(cls, _input: dict) -> Self:
        """Create Connection from dictionary"""
        return cls(
            id=_input.get("id"),
            createdAt=_input.get("createdAt"),
            notes=_input.get("notes", ''),
        )


@dataclass
class Person:
    """Dataclass for Person db object"""
    id: str
    relationshipType: RelationshipType
    frequencyDays: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    @classmethod
    def from_dict(cls, _input: dict) -> Self:
        """Create Person from dictionary"""
        return cls(
            id=_input.get('id'),
            relationshipType=_input.get('relationshipType'),
            frequencyDays=_input.get('frequencyDays'),
            firstName=_input.get('firstName', None),
            lastName=_input.get('lastName', None),
        )


@dataclass
class User:
    """Data class for User db object"""
    id: str
    email: str
    firstName: str
    lastName: str
    createdAt: int
    updatedAt: Optional[int] = None

    @classmethod
    def from_dict(cls, _input: dict) -> Self:
        """Create User from dictionary/json"""
        return cls(
            id=_input.get('id'),
            firstName=_input.get('firstName'),
            lastName=_input.get('lastName'),
            email=_input.get('email'),
            createdAt=_input.get('createdAt'),
            updatedAt=_input.get('updatedAt', None),
        )
