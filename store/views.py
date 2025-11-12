# store/views.py
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product

def product_list(request):
    q = (request.GET.get("q") or "").strip()
    searched = bool(q)

    qs = Product.objects.all().order_by("-created_at")

    if searched:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(image_url__icontains=q)
        )

    # ---- Pagination ----
    page_size = 12                          # tweak how many cards per page
    paginator = Paginator(qs, page_size)
    page = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Preserve current querystring (except page) in pagination links
    params = request.GET.copy()
    params.pop("page", None)
    base_qs = params.urlencode()  # e.g. "q=iphone"

    context = {
        "products": page_obj.object_list,   # current page items
        "page_obj": page_obj,               # for controls
        "paginator": paginator,
        "query": q,
        "searched": searched,
        "result_count": qs.count(),
        "base_qs": base_qs,
    }
    return render(request, "products/product_list.html", context)
