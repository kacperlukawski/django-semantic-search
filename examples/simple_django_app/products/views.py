from django.http import JsonResponse
from products.documents import ProductDocument


def index(request):
    """
    View for the index page.
    :param request: request object.
    :return: response object.
    """
    user_query = request.GET.get("query", "hello, world!")
    name_results = ProductDocument.objects.find(name=user_query)
    description_results = ProductDocument.objects.find(description=user_query)
    return JsonResponse(
        {
            "message": "Hello, world!",
            "name_results": list(name_results.values()),
            "description_results": list(description_results.values()),
        }
    )
