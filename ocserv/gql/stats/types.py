import graphene
from graphene_django import DjangoObjectType

from backend.internal.generics import PaginationResponseType
from ocserv.models import MonthlyTrafficStat


class TrafficStatsType(DjangoObjectType):

    class Meta:
        model = MonthlyTrafficStat
        fields = "__all__"


class TrafficStatsListType(graphene.ObjectType):
    statistics = graphene.List(TrafficStatsType)
    pagination = graphene.Field(PaginationResponseType)
