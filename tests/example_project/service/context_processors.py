from ella.core.models import Category

categories = sorted(Category.objects.all())

def simple_debug(request):
    return {'categories': categories,
            'request': request}
