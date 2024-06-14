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


class PaginationInputType(graphene.InputObjectType):
    page = graphene.Int(required=True)
    per_page = graphene.Int(required=True)


class PaginationResponseType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    per_page = graphene.Int()
    total_items = graphene.Int()
