import graphene
from graphql_jwt.decorators import login_required

from backend.internal.generics import PaginationInputType
from backend.internal.utils import pagination
from ocserv.gql.stats.types import TrafficStatsListType
from ocserv.models import MonthlyTrafficStat


class TrafficStatsQuery(graphene.ObjectType):
    ocserv_users_stats = graphene.Field(
        TrafficStatsListType,
        page_data=graphene.Argument(PaginationInputType, required=True),
        ocserv_user_id=graphene.ID(required=False),
    )

    @staticmethod
    @login_required
    def resolve_ocserv_users_stats(
        root, info, page_data: PaginationInputType, ocserv_user_id: id = None
    ) -> TrafficStatsListType:
        queryset = MonthlyTrafficStat.objects.all()
        if ocserv_user_id is not None:
            queryset = queryset.filter(user_id=ocserv_user_id)
        new_queryset, pagination_detail = pagination(queryset, page_data)
        return TrafficStatsListType(statistics=new_queryset, pagination=pagination_detail)
