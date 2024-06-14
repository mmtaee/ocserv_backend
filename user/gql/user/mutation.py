import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse, Response, ResponseOrError
from user.gql.user.types import UserInput


class CreateAdminUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        data = UserInput(required=True)

    @staticmethod
    def mutate(root, info, data: UserInput) -> ResponseOrError:
        user, create = User.objects.get_or_create(
            username=data.username,
            defaults={"password": make_password(data.password), "is_superuser": True},
        )
        if create:
            return Response(
                message="Admin User created successfully",
                metadata={"user": {"username": user.username, "is_superuser": user.is_superuser}},
            )
        return ErrorResponse(status="400", message="Admin user is Already exists")


class CreateStaffUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        data = UserInput(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, data: UserInput) -> ResponseOrError:
        user, create = User.objects.get_or_create(
            username=data.username,
            defaults={"password": make_password(data.password), "is_superuser": False},
        )
        if create:
            return Response(
                message="Staff User created successfully",
                metadata={"user": {"username": user.username, "is_superuser": user.is_superuser}},
            )
        return ErrorResponse(status="400", message="Staff user is Already exists")


class UpdateStaffUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        pk = graphene.ID(required=True)
        data = UserInput(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, pk: int, data: UserInput) -> Response:
        if not info.context.user.is_superuser:
            return ErrorResponse(
                status=403, message="You do not have permission to perform this action"
            )
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return ErrorResponse(status=404, message="User matching query does not exist.")
        for key, val in data.__dict__.items():
            if val is not None:
                setattr(user, key, val)
        user.save()
        return Response(
            message="User Updated successfully",
            metadata={
                "user_id": pk,
                "username": user.username,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
            },
        )


class DeleteStaffUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        pk = graphene.ID(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, pk: int) -> ResponseOrError:
        if not info.context.user.is_superuser:
            return ErrorResponse(
                status=403, message="You do not have permission to perform this action"
            )
        try:
            User.objects.get(pk=pk, is_superuser=False).delete()
            return Response(message="Staff User deleted successfully", metadata={"user_id": pk})
        except User.DoesNotExist:
            return ErrorResponse(status=404, message="User matching query does not exist.")
