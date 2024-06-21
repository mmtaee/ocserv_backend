import graphene
from django.db.models import FloatField, Sum
from django.db.models.functions import Coalesce
from graphql_jwt.decorators import login_required

from backend.internal.generics import PaginationInputType
from backend.internal.utils import pagination
from ocserv.gql.stats.types import StatDateType, TrafficStatsListType
from ocserv.models import MonthlyTrafficStat


class TrafficStatsQuery(graphene.ObjectType):
    ocserv_users_stats = graphene.Field(
        TrafficStatsListType,
        page_data=graphene.Argument(PaginationInputType, required=True),
        date=graphene.Argument(StatDateType, required=False),
        ocserv_user_id=graphene.ID(required=False),
    )

    @staticmethod
    @login_required
    def resolve_ocserv_users_stats(
        root,
        info,
        page_data: PaginationInputType,
        ocserv_user_id: id = None,
        date: StatDateType = None,
    ) -> TrafficStatsListType:
        queryset = MonthlyTrafficStat.objects.all()
        if ocserv_user_id is not None:
            queryset = queryset.filter(user_id=ocserv_user_id)
        if date is not None:
            queryset = queryset.filter(month=date.month, year=date.year)
        new_queryset, pagination_detail = pagination(queryset, page_data)
        total = new_queryset.aggregate(
            total_rx=Coalesce(Sum("rx"), 0, output_field=FloatField()),
            total_tx=Coalesce(Sum("tx"), 0, output_field=FloatField()),
        )
        return TrafficStatsListType(
            statistics=new_queryset,
            pagination=pagination_detail,
            total_rx=total["total_rx"],
            total_tx=total["total_tx"],
        )
