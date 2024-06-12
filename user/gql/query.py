import graphene
from graphql_jwt.decorators import login_required

from user.gql.types import ConfigType, UserType
from user.models import Config


class ConfigQuery(graphene.ObjectType):
    site_config = graphene.Field(ConfigType)

    @staticmethod
    def resolve_site_config(root, info):
        return Config.objects.last()


class Profile(graphene.ObjectType):
    profile = graphene.Field(UserType)

    @staticmethod
    @login_required
    def resolve_profile(root, info):
        return info.context.user
