import graphene
from graphql_jwt.decorators import login_required

from backend.internal.generics import PaginationInputType, PaginationResponseType
from backend.internal.utils import pagination
from ocserv.gql.user.types import OcservUserListType
from ocserv.models import OcservUser


class OcservUserQuery(graphene.ObjectType):
    ocserv_users = graphene.Field(
        OcservUserListType, page_data=graphene.Argument(PaginationInputType, required=True)
    )

    @staticmethod
    @login_required
    def resolve_ocserv_users(root, info, page_data: PaginationInputType) -> OcservUserListType:
        queryset = OcservUser.objects.all()
        new_queryset, pagination_detail = pagination(queryset, page_data)
        return OcservUserListType(ocserv_users=new_queryset, pagination=pagination_detail)
