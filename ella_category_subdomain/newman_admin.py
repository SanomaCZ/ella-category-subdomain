from ella import newman

from ella_category_subdomain.models import CategorySubdomain


class CategorySubdomainAdmin(newman.NewmanModelAdmin):
    pass

newman.site.register(CategorySubdomain, CategorySubdomainAdmin)
