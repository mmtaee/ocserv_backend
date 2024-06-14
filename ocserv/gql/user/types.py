import graphene
from graphene_django.types import DjangoObjectType

from backend.internal.generics import PaginationResponseType
from ocserv.models import OcservUser


class OcservTrafficEnum(graphene.Enum):
    FREE = 1
    MONTHLY = 2
    TOTALLY = 3


class OcservUserType(DjangoObjectType):

    class Meta:
        model = OcservUser
        fields = "__all__"


class OcservUserListType(graphene.ObjectType):
    ocserv_users = graphene.List(OcservUserType)
    pagination = graphene.Field(PaginationResponseType)
