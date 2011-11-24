from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Ella fallback for everything else
    (r'^', include('ella.core.urls')),
)
