import graphene
from graphene_django.types import DjangoObjectType

from ocserv.models import OcservUser


class OcservTrafficEnum(graphene.Enum):
    FREE = 1
    MONTHLY = 2
    TOTALLY = 3


class OcservUserType(DjangoObjectType):

    class Meta:
        model = OcservUser
        fields = "__all__"


class PaginationInputType(graphene.InputObjectType):
    page = graphene.Int(required=True)
    per_page = graphene.Int(required=True)


class PaginationResponseType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    per_page = graphene.Int()
    total_items = graphene.Int()


class OcservUserListType(graphene.ObjectType):
    ocserv_users = graphene.List(OcservUserType)
    pagination = graphene.Field(PaginationResponseType)
