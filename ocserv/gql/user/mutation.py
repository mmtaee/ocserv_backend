import graphene
from django.forms import model_to_dict
from graphql_jwt.decorators import login_required

from backend.internal.generics import ErrorResponse, Response, ResponseOrError
from backend.internal.occtl.user import OcctlUser
from ocserv.gql.user.types import OcservTrafficEnum, OcservUserFormInput, OcservUserUpdateFormInput
from ocserv.models import OcservUser


class CreateOcservUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        data = OcservUserFormInput(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, data) -> ResponseOrError:
        if OcservUser.objects.filter(username=data.username).exists():
            return ErrorResponse(message="Ocserv User already exists", status=400)
        data.traffic = data.pop("traffic").value
        ocserv_user = OcservUser.objects.create(**data.__dict__)
        return Response(
            message="Ocserv User created successfully", metadata=model_to_dict(ocserv_user)
        )


class UpdateOcservUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        data = OcservUserUpdateFormInput(required=False)
        pk = graphene.ID(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, pk: int, data) -> ResponseOrError:
        try:
            ocserv_user = OcservUser.objects.get(pk=pk)
        except OcservUser.DoesNotExist:
            return ErrorResponse(message="Ocserv User does not exists", status=404)
        if data.traffic:
            data.traffic = data.pop("traffic").value
        for k, v in data.__dict__.items():
            if v is not None:
                setattr(ocserv_user, k, v)
        ocserv_user.save()
        return Response(
            message="Ocserv User updated successfully",
            metadata={
                "id": ocserv_user.id,
                "username": ocserv_user.username,
                "lock": ocserv_user.lock,
            },
        )


class DeleteOcservUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        pk = graphene.ID(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, pk: int) -> ResponseOrError:
        try:
            ocserv_user = OcservUser.objects.get(pk=pk)
        except OcservUser.DoesNotExist:
            return ErrorResponse(message="Ocserv User does not exists", status=404)
        ocserv_user.delete()
        return Response(
            message="Ocserv User deleted successfully",
            metadata={"id": ocserv_user.id, "username": ocserv_user.username},
        )


class DisconnectOcservUser(graphene.Mutation):
    Output = ResponseOrError

    class Arguments:
        pk = graphene.ID(required=True)

    @staticmethod
    @login_required
    def mutate(root, info, pk: int) -> ResponseOrError:
        try:
            ocserv_user = OcservUser.objects.get(pk=pk)
        except OcservUser.DoesNotExist:
            return ErrorResponse(message="Ocserv User does not exists", status=404)
        occtl_user = OcctlUser(username=ocserv_user.username)
        result = occtl_user.disconnect()
        return Response(
            message=f"Request Disconnected user {ocserv_user.username} send to sever",
            metadata={"result": result},
        )


class SyncOcservUser(graphene.Mutation):
    Output = Response

    class Arguments:
        traffic = graphene.Argument(OcservTrafficEnum, required=False)
        default_traffic = graphene.Int(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, traffic=OcservTrafficEnum.FREE, default_traffic: int = 10) -> Response:
        occtl_user = OcctlUser()
        results = occtl_user.sync()
        usernames = [u.get("username") for u in results]
        locked_users = [u.get("username") for u in results if u.get("lock")]
        existing_users = set(
            OcservUser.objects.filter(username__in=usernames).values_list("username", flat=True)
        )
        new_users = []
        for username in usernames:
            if username not in existing_users:
                new = OcservUser.objects.create(
                    username=username,
                    password="Hashed by ocpasswd command",
                    traffic=traffic.value,
                    default_traffic=default_traffic,
                    lock=username in locked_users,
                )
                new_users.append(
                    {"username": new.username, "password": new.password, "lock": new.lock}
                )
        return Response(
            message=f"Sync ocpasswd-file done successfully", metadata={"new_users": new_users}
        )
