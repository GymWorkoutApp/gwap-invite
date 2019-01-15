from typing import Dict
from uuid import uuid4

from gwap_framework.resource.base import BaseResource
from gwap_framework.utils.decorators import validate_schema

from src.cache import cache
from src.database import master_async_session, read_replica_async_session
from src.models import InviteModel
from src.schemas import InviteInputSchema, InviteOutputSchema


class InviteResource(BaseResource):
    cache = cache
    method_decorators = {
        'create': [validate_schema(InviteInputSchema)],
        'update': [validate_schema(InviteInputSchema)],
    }

    def create(self, request_model: 'InviteInputSchema') -> Dict:
        invite = InviteModel()
        invite.id = request_model.invite_id or str(uuid4())
        invite.owner_id = request_model.owner_id
        invite.guest_id = request_model.guest_id
        invite.guest_type = request_model.guest_type

        with master_async_session() as session:
            session.add(invite)
            output = InviteOutputSchema()
            output.invite_id = invite.id
            output.owner_id = invite.owner_id
            output.guest_id = invite.guest_id
            output.guest_type = invite.guest_type
            output.status = invite.status
            output.validate()
            return output.to_primitive()

    def update(self, request_model: 'InviteInputSchema', invite_id=None):
        invite = InviteModel()
        invite.id = invite_id
        invite.owner_id = request_model.owner_id
        invite.guest_id = request_model.guest_id
        invite.guest_type = request_model.guest_type
        invite.status = request_model.status

        with master_async_session() as session:
            session.merge(invite)
            output = InviteOutputSchema()
            output.invite_id = invite.id
            output.owner_id = invite.owner_id
            output.guest_id = invite.guest_id
            output.guest_type = invite.guest_type
            output.status = invite.status
            output.validate()
            return output.to_primitive()

    def list(self, args=None, kwargs=None):
        with read_replica_async_session() as session:
            results = []
            for invite in session.query(InviteModel).all():
                output = InviteOutputSchema()
                output.invite_id = invite.id
                output.owner_id = invite.owner_id
                output.guest_id = invite.guest_id
                output.guest_type = invite.guest_type
                output.status = invite.status
                output.validate()
                results.append(output.to_primitive())
        return results

    def retrieve(self, invite_id):
        with read_replica_async_session() as session:
            invite = session.query(InviteModel).filter_by(id=invite_id).first()
            output = InviteOutputSchema()
            output.invite_id = invite.id
            output.owner_id = invite.owner_id
            output.guest_id = invite.guest_id
            output.guest_type = invite.guest_type
            output.status = invite.status
            output.validate()
            return output.to_primitive()

    def destroy(self, invite_id):
        with master_async_session() as session:
            session.query(InviteModel).filter_by(id=invite_id).delete()
            return None


resources_v1 = [
    {'resource': InviteResource, 'urls': ['/invites/<invite_id>'], 'endpoint': 'Invites InviteId',
     'methods': ['GET', 'PUT', 'PATCH', 'DELETE']},
    {'resource': InviteResource, 'urls': ['/invites'], 'endpoint': 'Invites',
     'methods': ['POST', 'GET']},
]
