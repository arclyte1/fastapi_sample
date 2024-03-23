from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref

Base = declarative_base()


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    participants: Mapped[List["Participant"]] = relationship(
        backref=backref("group"), cascade="all,delete"
    )

    def __repr__(self):
        return f"Group(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Participant(Base):
    __tablename__ = "participant"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    wish: Mapped[str | None] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    recipient_id: Mapped[int | None] = mapped_column(ForeignKey("participant.id", ondelete="SET NULL"))
    recipient: Mapped["Participant"] = relationship(remote_side=[id])

    def __repr__(self):
        return f"Participant(id={self.id!r}, name={self.name!r}), wish={self.wish!r}"
