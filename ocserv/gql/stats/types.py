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
    total_rx = graphene.Float(default_value=0, description="Total rx Traffic Stats")
    total_tx = graphene.Float(default_value=0, description="Total tx Traffic Stats")
    pagination = graphene.Field(PaginationResponseType)


class StatDateType(graphene.InputObjectType):
    month = graphene.Int()
    year = graphene.Int()
