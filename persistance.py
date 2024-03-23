import os
import random

from sqlalchemy import select, create_engine, update, delete
from sqlalchemy.orm import sessionmaker, joinedload

from dto import CreateGroup, CreateParticipant
from models import Base, Group, Participant

engine = create_engine(os.environ["POSTGRES_URL"])
Session = sessionmaker(bind=engine, autoflush=False)
Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def map_row(data):
    return data[0].__dict__


def map_row_list(data):
    return list(map(lambda x: map_row(x), data))


def create_group(data: CreateGroup) -> Group:
    db = next(get_db())
    group = Group(name=data.name, description=data.description)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_groups():
    db = next(get_db())
    groups = db.scalars(select(Group)).all()
    return groups


def get_group_details(id: int):
    db = next(get_db())
    group = db.scalar(select(Group).where(Group.id == id).options(joinedload(Group.participants)))
    return group


def create_participant(data: CreateParticipant, group_id: int):
    db = next(get_db())
    participant = Participant(name=data.name, wish=data.wish, group_id=group_id)
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def group_toss(id: int):
    db = next(get_db())
    participants = list(db.scalars(select(Participant).where(Participant.group_id == id)).all())
    if len(participants) >= 3:
        random.shuffle(participants)
        for i in range(len(participants) - 1):
            db.execute(update(Participant).where(Participant.id == participants[i].id)
                       .values(recipient_id=participants[i + 1].id))
        db.execute(update(Participant)
                   .where(Participant.id == participants[-1].id)
                   .values(recipient_id=participants[0].id))
        db.commit()
        return db.scalars(select(Participant).where(Participant.group_id == id)).all()


def update_group(id: int, data: dict):
    db = next(get_db())
    if "name" in data and data["name"] is not None:
        db.execute(update(Group).where(Group.id == id).values(name=data["name"]))
    if "description" in data:
        db.execute(update(Group).where(Group.id == id).values(name=data["name"]))
    db.commit()
    return get_group_details(id)


def delete_group(id: int):
    db = next(get_db())
    exists = db.scalar(select(Group).where(Group.id == id))
    db.execute(delete(Group).where(Group.id == id))
    db.commit()
    return bool(exists)


def delete_participant(group_id: int, participant_id: int):
    db = next(get_db())
    exists = db.scalar(select(Participant).where(Participant.id == participant_id and Participant.group_id == group_id))
    db.execute(delete(Participant).where(Participant.id == participant_id and Participant.group_id == group_id))
    db.commit()
    return bool(exists)


def get_recipient(group_id: int, participant_id: int):
    db = next(get_db())
    participant = db.scalar(
        select(Participant).where(Participant.id == participant_id and Participant.group_id == group_id))
    return participant.recipient
