import graphene
from graphene.types import generic


class Response(graphene.ObjectType):
    message = graphene.String()
    metadata = generic.GenericScalar(description="Additional metadata")


class ErrorResponse(graphene.ObjectType):
    status = graphene.Int()
    message = graphene.String(description="Error message response.")


class ResponseOrError(graphene.Union):
    class Meta:
        types = (Response, ErrorResponse)
