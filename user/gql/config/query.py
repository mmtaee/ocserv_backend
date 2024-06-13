import graphene

from user.gql.config.types import ConfigType
from user.models import Config


class ConfigQuery(graphene.ObjectType):
    site_config = graphene.Field(ConfigType)

    @staticmethod
    def resolve_site_config(root, info):
        return Config.objects.last()
