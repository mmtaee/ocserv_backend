import graphene
from django.forms import ModelForm
from graphene_django.forms.types import DjangoFormInputObjectType
from graphene_django.types import DjangoObjectType

from backend.internal.generics import ErrorResponse, PaginationResponseType
from ocserv.models import OcservUser


class OcservTrafficEnum(graphene.Enum):
    FREE = 1
    MONTHLY = 2
    TOTALLY = 3


class OcservUserType(DjangoObjectType):
    traffic_display = graphene.String()

    class Meta:
        model = OcservUser
        fields = "__all__"
        convert_choices_to_enum = False

    @staticmethod
    def resolve_traffic_display(root, info):
        return root.get_traffic_display()


class OcservUserListType(graphene.ObjectType):
    ocserv_users = graphene.List(OcservUserType)
    pagination = graphene.Field(PaginationResponseType)


class OcservUserOrErrorResponse(graphene.Union):
    class Meta:
        types = (OcservUserType, ErrorResponse)


class OcservUserForm(ModelForm):
    class Meta:
        model = OcservUser
        exclude = ("id", "deactivate_date", "rx", "tx", "traffic")


class OcservUserFormInput(DjangoFormInputObjectType):
    traffic = OcservTrafficEnum(required=True)

    class Meta:
        form_class = OcservUserForm
        object_type = OcservUserType


class OcservUserUpdateForm(ModelForm):
    class Meta:
        model = OcservUser
        exclude = ("id", "deactivate_date", "rx", "tx", "traffic")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class OcservUserUpdateFormInput(DjangoFormInputObjectType):
    traffic = OcservTrafficEnum(required=False)

    class Meta:
        form_class = OcservUserUpdateForm
        object_type = OcservUserType
