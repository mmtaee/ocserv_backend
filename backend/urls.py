from django.conf import settings
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path(
        "api/gql/", GraphQLView.as_view(graphiql=True if settings.DEBUG else False), name="graphql"
    )
]


if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]
