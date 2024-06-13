import graphene


class OnlineUserType(graphene.ObjectType):
    username = graphene.String()
    host = graphene.String()
    remote_ip = graphene.String()
    since = graphene.String()
    averages = graphene.String()


class IroutesType(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    vhost = graphene.String()
    device = graphene.String()
    ip = graphene.String()
    iroutes = graphene.String()


class IPBansType(graphene.ObjectType):
    ip = graphene.String()
    since = graphene.String()
    score = graphene.String()


class DashboardType(graphene.ObjectType):
    online_users = graphene.List(OnlineUserType)
    ip_bans = graphene.List(IPBansType)
    iroutes = graphene.List(IroutesType)
    status = graphene.String()
