import graphene
import graphql_jwt

from ocserv.schema import Mutation as OcservMutation
from ocserv.schema import Query as OcservQuery
from user.schema import Mutation as UserMutation
from user.schema import Query as UserQuery


class Query(UserQuery, OcservQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, OcservMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.relay.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
