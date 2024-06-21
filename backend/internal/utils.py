from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet

from backend.internal.generics import PaginationInputType as PaginationInput
from backend.internal.generics import PaginationResponseType as PaginationResponse


def pagination(queryset: QuerySet, p: PaginationInput) -> tuple[QuerySet, PaginationResponse]:
    total_items = queryset.count()
    if p.per_page > 100:
        p.per_page = 50
    if p.per_page == 0 or total_items == 0:
        return queryset, PaginationResponse(
            page=1, per_page=p.per_page, pages=1, total_items=total_items
        )
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
    return obj, PaginationResponse(
        page=p.page, per_page=p.per_page, pages=pages, total_items=total_items
    )
