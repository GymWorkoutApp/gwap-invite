import enum
from uuid import uuid4

from gwap_framework.models.base import BaseModel
from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID


class GuestType(enum.Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'


class InviteStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DENIED = 'denied'


class InviteModel(BaseModel):
    __tablename__ = 'invites'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    guest_id = Column(UUID(as_uuid=True), nullable=False)
    guest_type = Column(Enum(GuestType), nullable=False)
    status = Column(Enum(GuestType), nullable=False, default=InviteStatus.PENDING)
