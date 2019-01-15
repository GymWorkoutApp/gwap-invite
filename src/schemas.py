from gwap_framework.schemas.base import BaseSchema
from schematics.types import StringType

from src.models import InviteStatus


class InviteInputSchema(BaseSchema):
    invite_id = StringType(required=False, serialized_name='inviteId')
    owner_id = StringType(required=True, serialized_name='ownerId')
    guest_id = StringType(required=True, serialized_name='guestId')
    guest_type = StringType(required=True, serialized_name='guestType')
    status = StringType(required=False, choices=[InviteStatus.PENDING, InviteStatus.ACCEPTED, InviteStatus.DENIED])


class InviteOutputSchema(BaseSchema):
    invite_id = StringType(required=True, serialized_name='inviteId')
    owner_id = StringType(required=True, serialized_name='ownerId')
    guest_id = StringType(required=True, serialized_name='guestId')
    guest_type = StringType(required=True, serialized_name='guestType')
    status = StringType(required=True, choices=[InviteStatus.PENDING, InviteStatus.ACCEPTED, InviteStatus.DENIED])
