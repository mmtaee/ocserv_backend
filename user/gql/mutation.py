import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import model_to_dict
from graphql_jwt.decorators import login_required

from backend.generics import ErrorResponse, Response, ResponseOrError
from user.gql.types import ConfigInput, UserInput
from user.models import Config


class CreateConfig(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        data = ConfigInput(required=False)

    @staticmethod
    def mutate(root, info, data: ConfigInput) -> ResponseOrError:
        if Config.objects.exists():
            return ErrorResponse(status=403, message="Config is configured")
        config = Config.objects.create(**data)
        return Response(
            message="config created successfully",
            metadata={"config": model_to_dict(config)},
        )


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
                metadata={
                    "user": {"username": user.username, "is_superuser": user.is_superuser}
                },
            )
        return ErrorResponse(status="403", message="Admin user is Already exists")


class UpdateConfig(graphene.Mutation):
    class Arguments:
        data = ConfigInput(required=False)

    Output = Response

    @staticmethod
    @login_required
    def mutate(root, info, data: ConfigInput) -> Response:
        obj = Config.objects.last()
        for key, val in data.__dict__.items():
            if val is not None:
                setattr(obj, key, val)
        obj.save()
        return Response(message="Config Updated successfully")
