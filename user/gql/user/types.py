import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

from backend.internal.generics import ErrorResponse


class LoginInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()
    is_active = graphene.Boolean(default_value=True)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "is_superuser")


class Staffs(graphene.ObjectType):
    staffs = graphene.List(UserType)


class UserOrErrorResponse(graphene.Union):
    class Meta:
        types = (Staffs, ErrorResponse)
