from typing import List

from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str
    description: str | None = None


class CreateParticipant(BaseModel):
    name: str
    wish: str | None = None


class ParticipantDto(BaseModel):
    id: int
    name: str
    wish: str | None

    class Config:
        orm_mode = True


class ParticipantDetailsDto(BaseModel):
    id: int
    name: str
    wish: str | None
    recipient: ParticipantDto | None

    class Config:
        orm_mode = True


class GroupDetailsDto(BaseModel):
    id: int
    name: str
    description: str | None
    participants: List[ParticipantDetailsDto]

    class Config:
        orm_mode = True


class GroupDto(BaseModel):
    id: int
    name: str
    description: str | None
