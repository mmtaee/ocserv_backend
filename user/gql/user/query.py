from typing import List, Union

import graphene
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse
from user.gql.user.types import Staffs, UserOrErrorResponse, UserType


class ProfileQuery(graphene.ObjectType):
    profile = graphene.Field(UserType)

    @staticmethod
    @login_required
    def resolve_profile(root, info):
        return info.context.user


class StaffsQuery(graphene.ObjectType):
    staffs = graphene.Field(UserOrErrorResponse)

    @staticmethod
    def resolve_staffs(root, info) -> Union[List[Staffs], ErrorResponse]:
        if info.context.user.is_superuser:
            return Staffs(User.objects.filter(is_superuser=False))
        return ErrorResponse(
            status=403, message="You do not have permission to perform this action"
        )
