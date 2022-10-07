from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginateProducts(request, products, results):
    page = request.GET.get('page')

    paginator = Paginator(products, results)

    products = paginator.get_page(page)

    return products
