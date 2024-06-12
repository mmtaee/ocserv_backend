import graphene

from user.gql.mutation import CreateAdminUser, CreateConfig, UpdateConfig
from user.gql.query import ConfigQuery, Profile


class Query(ConfigQuery, Profile):
    pass


class Mutation(graphene.ObjectType):
    create_config = CreateConfig.Field()
    create_admin_user = CreateAdminUser.Field()
    update_config = UpdateConfig.Field()
