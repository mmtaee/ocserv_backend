import graphene

from ocserv.gql.dashboard.query import DashboardQuery
from ocserv.gql.group.mutation import (
    CreateOcservGroup,
    DeleteOcservGroup,
    UpdateOcservDefaultGroup,
    UpdateOcservGroup,
)
from ocserv.gql.group.query import DefaultOcservGroupQuery, OcservGroupQuery
from ocserv.gql.stats.query import TrafficStatsQuery
from ocserv.gql.user.mutation import (
    CreateOcservUser,
    DeleteOcservUser,
    DisconnectOcservUser,
    SyncOcservUser,
    UpdateOcservUser,
)
from ocserv.gql.user.query import OcservUserDetailQuery, OcservUserQuery

queries = (
    DashboardQuery,
    DefaultOcservGroupQuery,
    OcservGroupQuery,
    OcservUserQuery,
    OcservUserDetailQuery,
    TrafficStatsQuery,
)


class Query(*queries):
    pass


class Mutation(graphene.ObjectType):
    # Ocserv Group
    update_ocserv_default_group = UpdateOcservDefaultGroup.Field()
    create_ocserv_group = CreateOcservGroup.Field()
    update_ocserv_group = UpdateOcservGroup.Field()
    delete_ocserv_group = DeleteOcservGroup.Field()

    # Ocserv User
    create_ocserv_user = CreateOcservUser.Field()
    update_ocserv_user = UpdateOcservUser.Field()
    delete_ocserv_user = DeleteOcservUser.Field()
    disconnect_ocserv_user = DisconnectOcservUser.Field()
    sync_ocserv_user = SyncOcservUser.Field()
