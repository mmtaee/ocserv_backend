import graphene
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse
from backend.internal.occtl.group import OcctlGroup
from ocserv.gql.group.types import GroupConfigOrErrorResponse, GroupConfigType

occtl_group = OcctlGroup()


class DefaultOcservGroupQuery(graphene.ObjectType):
    ocserv_default_group = graphene.Field(GroupConfigType)

    @staticmethod
    @login_required
    def resolve_ocserv_default_group(root, info) -> GroupConfigType:
        return occtl_group.get_default()


class OcservGroupQuery(graphene.ObjectType):
    ocserv_group = graphene.Field(
        GroupConfigOrErrorResponse, group_name=graphene.String(required=True)
    )

    @staticmethod
    @login_required
    def resolve_ocserv_group(root, info, group_name: str) -> GroupConfigOrErrorResponse:
        occtl_group.group_name = group_name
        if not occtl_group.group_exists():
            return ErrorResponse(message="Group does not exist", status=404)
        return GroupConfigType(**occtl_group.get_group())
