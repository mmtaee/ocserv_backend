import graphene
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse
from backend.internal.occtl.group import Group
from ocserv.gql.group.types import GroupConfigOrErrorResponse, GroupConfigType

ocserv_group = Group()


class DefaultGroupQuery(graphene.ObjectType):
    ocserv_default_group = graphene.Field(GroupConfigType)

    @staticmethod
    @login_required
    def resolve_ocserv_default_group(root, info) -> GroupConfigType:
        return ocserv_group.get_default()


class GroupQuery(graphene.ObjectType):
    ocserv_group = graphene.Field(
        GroupConfigOrErrorResponse, group_name=graphene.String(required=True)
    )

    @staticmethod
    @login_required
    def resolve_ocserv_group(root, info, group_name: str) -> GroupConfigOrErrorResponse:
        ocserv_group.group_name = group_name
        if not ocserv_group.group_exists():
            return ErrorResponse(message="Group does not exist", status=404)
        return GroupConfigType(**ocserv_group.get_group())
