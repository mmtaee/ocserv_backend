from typing import AnyStr, Type

from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet

from ocserv.gql.user.types import PaginationInputType as PaginationInput
from ocserv.gql.user.types import PaginationResponseType as PaginationType


def group_config_repr(data: Type) -> tuple[list[AnyStr], dict]:
    configs = []
    metadata = {}
    for key, val in data.__dict__.items():
        if val is not None:
            if isinstance(val, bool):
                val = str(val).lower()
            configs.append(f"{key.replace('_', '-').lower()}={val}")
            metadata[key] = val
    return configs, metadata


def pagination(queryset: QuerySet, p: PaginationInput) -> tuple[QuerySet, dict[str, AnyStr]]:
    total_items = queryset.count()
    if p.per_page == 0 or total_items == 0:
        return queryset, {"page": 1, "per_page": 50, "pages": 1, "total_items": total_items}
    if p.per_page > 100:
        p.per_page = 50
    if total_items <= p.per_page:
        p.per_page = total_items
    if not queryset.ordered:
        queryset = queryset.order_by("id")
    paginator = Paginator(queryset, p.per_page)
    try:
        obj = paginator.page(p.page).object_list
    except ZeroDivisionError:
        return queryset.none(), 0
    except (EmptyPage, PageNotAnInteger, InvalidPage):
        obj = paginator.page(1).object_list
    pages = paginator.num_pages
    if pages in [0, 1]:
        pages = 1
    return obj, {
        "page": p.page,
        "per_page": p.per_page,
        "pages": pages,
        "total_items": total_items,
    }
