import graphene

from ocserv.gql.dashboard.query import DashboardQuery
from ocserv.gql.group.mutation import (
    CreateOcservGroup,
    DeleteOcservGroup,
    UpdateOcservDefaultGroup,
    UpdateOcservGroup,
)
from ocserv.gql.group.query import DefaultGroupQuery, GroupQuery

queries = (DashboardQuery, DefaultGroupQuery, GroupQuery)


class Query(*queries):
    pass


class Mutation(graphene.ObjectType):
    update_ocserv_default_group = UpdateOcservDefaultGroup.Field()
    create_ocserv_group = CreateOcservGroup.Field()
    update_ocserv_group = UpdateOcservGroup.Field()
    delete_ocserv_group = DeleteOcservGroup.Field()
