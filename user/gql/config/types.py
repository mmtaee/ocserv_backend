import graphene
from graphene_django import DjangoObjectType

from user.models import Config


class ConfigInput(graphene.InputObjectType):
    captcha_site_key = graphene.String()
    captcha_secret_key = graphene.String()
    default_traffic = graphene.Int()


class ConfigType(DjangoObjectType):

    class Meta:
        model = Config
        exclude = ("id",)
