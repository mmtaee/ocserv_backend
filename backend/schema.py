import graphene
import graphql_jwt

from user.schema import Mutation as UserMutation
from user.schema import Query as UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.relay.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
