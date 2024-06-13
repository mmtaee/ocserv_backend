import graphene
from django.forms import model_to_dict
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse, Response, ResponseOrError
from user.gql.config.types import ConfigInput
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


class UpdateConfig(graphene.Mutation):
    class Arguments:
        data = ConfigInput(required=False)

    Output = Response

    @staticmethod
    @login_required
    def mutate(root, info, data: ConfigInput) -> ResponseOrError:
        config = Config.objects.last()
        for key, val in data.__dict__.items():
            if val is not None:
                setattr(config, key, val)
        config.save()
        return Response(message="Config Updated successfully")
