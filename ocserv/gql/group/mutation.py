import graphene
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse, Response, ResponseOrError
from backend.internal.occtl.group import OcctlGroup
from ocserv.gql.group.types import ConfigInputType
from ocserv.gql.group.utils import group_config_repr

occtl_group = OcctlGroup()


class UpdateOcservDefaultGroup(graphene.Mutation):
    Output = Response

    class Arguments:
        data = ConfigInputType(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, data: ConfigInputType) -> Response:
        configs, metadata = group_config_repr(data)
        occtl_group.update_default(configs)
        return Response(message="Config updated successfully", metadata=metadata)


class CreateOcservGroup(graphene.Mutation):
    """
    Create a group or update an existing group's configuration.

    If a group with the same name already exists, this function updates its configuration
    rather than creating a new group.
    """

    Output = Response

    class Arguments:
        name = graphene.String(required=True)
        data = ConfigInputType(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, name: str, data: ConfigInputType) -> Response:
        configs, _ = group_config_repr(data)
        occtl_group.group_name = name
        occtl_group.create_or_update_group(configs)
        return Response(message="Group created successfully", metadata={"group_name": name})


class UpdateOcservGroup(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        group_name = graphene.String(required=True)
        data = ConfigInputType(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, data: ConfigInputType, group_name: str) -> Response:
        occtl_group.group_name = group_name
        if not occtl_group.group_exists():
            return ErrorResponse(message="Group does not exist", status=404)
        configs, metadata = group_config_repr(data)
        occtl_group.create_or_update_group(configs)
        return Response(message="Config updated successfully", metadata=metadata)


class DeleteOcservGroup(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        group_name = graphene.String(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, group_name: str) -> ResponseOrError:
        if group_name == "defaults":
            return ErrorResponse(
                status=400, message="You are not allowed to delete the defaults ocserv group"
            )
        occtl_group.group_name = group_name
        if not occtl_group.group_exists():
            return ErrorResponse(message="Group does not exist", status=404)
        occtl_group.delete_group()
        return Response(
            message=f"Ocserv group({group_name}) deleted successfully",
            metadata={"group_name": group_name},
        )
