import graphene

from user.gql.config.mutation import CreateConfig, UpdateConfig
from user.gql.config.query import ConfigQuery
from user.gql.user.mutation import (
    CreateAdminUser,
    CreateStaffUser,
    DeleteStaffUser,
    UpdateStaffUser,
)
from user.gql.user.query import ProfileQuery, StaffsQuery

queries = (ConfigQuery, ProfileQuery, StaffsQuery)


class Query(*queries):
    pass


class Mutation(graphene.ObjectType):
    create_config = CreateConfig.Field()
    create_admin_user = CreateAdminUser.Field()
    update_config = UpdateConfig.Field()
    create_staff_user = CreateStaffUser.Field()
    update_staff_user = UpdateStaffUser.Field()
    delete_staff_user = DeleteStaffUser.Field()
