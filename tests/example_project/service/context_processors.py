from ella.core.models import Category

_categories = sorted(Category.objects.all())

def categories(request):
    return {'categories': _categories}
