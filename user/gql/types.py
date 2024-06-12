import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

from user.models import Config


class LoginInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class ConfigInput(graphene.InputObjectType):
    captcha_site_key = graphene.String()
    captcha_secret_key = graphene.String()
    default_traffic = graphene.Int()


class ConfigType(DjangoObjectType):

    class Meta:
        model = Config
        exclude = ("id",)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "is_superuser")
