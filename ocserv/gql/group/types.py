import graphene

from backend.internal.generics import ErrorResponse


class GroupConfigType(graphene.ObjectType):
    rx_data_per_sec = graphene.String(description="RX data bytes per second")
    tx_data_per_sec = graphene.String(description="TX data bytes per second")
    max_same_clients = graphene.String(description="Maximum session number of clients")
    ipv4_network = graphene.String()
    dns1 = graphene.String()
    dns2 = graphene.String()
    no_udp = graphene.String(description="Disable UDP connection")
    keepalive = graphene.String(description="Keep alive user session per seconds")
    dpd = graphene.String(description="DPD per seconds")
    mobile_dpd = graphene.String(description="Mobile DPD per seconds")
    tunnel_all_dns = graphene.String(description="Tunnel all DNS servers")
    restrict_user_to_routes = graphene.String(description="Restrict user to routes")
    stats_report_time = graphene.String(description="Statistics report time per seconds")
    mtu = graphene.String(description="MTU")
    idle_timeout = graphene.String(description="IDLE timeout per seconds")
    mobile_idle_timeout = graphene.String(description="Mobile IDLE timeout per seconds")
    session_timeout = graphene.String(description="Session timeout per seconds")
    no_routes = graphene.List(graphene.String)
    routes = graphene.List(graphene.String)


class ConfigInputType(graphene.InputObjectType):
    rx_data_per_sec = graphene.String(
        description="RX data bytes per second", required=False
    )
    tx_data_per_sec = graphene.String(
        description="TX data bytes per second", required=False
    )
    max_same_clients = graphene.String(
        description="Maximum session number of clients", required=False
    )
    ipv4_network = graphene.String(required=False)
    dns1 = graphene.String(required=False)
    dns2 = graphene.String(required=False)
    no_udp = graphene.Boolean(description="Disable UDP connection", required=False)
    keepalive = graphene.String(
        description="Keep alive user session per seconds", required=False
    )
    dpd = graphene.String(description="DPD per seconds", required=False)
    mobile_dpd = graphene.String(description="Mobile DPD per seconds", required=False)
    tunnel_all_dns = graphene.Boolean(
        description="Tunnel all DNS servers", required=False
    )
    restrict_user_to_routes = graphene.Boolean(
        description="Restrict user to routes", required=False
    )
    stats_report_time = graphene.String(
        description="Statistics report time per seconds", required=False
    )
    mtu = graphene.String(description="MTU")
    idle_timeout = graphene.String(description="IDLE timeout per seconds", required=False)
    mobile_idle_timeout = graphene.String(
        description="Mobile IDLE timeout per seconds", required=False
    )
    session_timeout = graphene.String(
        description="Session timeout per seconds", required=False
    )
    no_routes = graphene.List(graphene.String, required=False)
    routes = graphene.List(graphene.String, required=False)


class GroupConfigOrErrorResponse(graphene.Union):
    class Meta:
        types = (GroupConfigType, ErrorResponse)
