import graphene
from graphql_jwt.decorators import login_required

from backend.internal.occtl.system import Occtl
from ocserv.gql.dashboard.types import DashboardType

occtl = Occtl()


class DashboardQuery(graphene.ObjectType):
    dashboard = graphene.Field(DashboardType)

    @staticmethod
    @login_required
    def resolve_dashboard(root, info) -> DashboardType:
        return DashboardType(
            online_users=occtl.online_users,
            ip_bans=occtl.ip_bans,
            iroutes=occtl.iroutes,
            status=occtl.status,
        )
