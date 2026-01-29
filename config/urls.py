from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
except Exception:
    get_schema_view = None
    openapi = None
    permissions = None

spa_view = TemplateView.as_view(template_name="index.html")

schema_view = None
if get_schema_view is not None:
    schema_view = get_schema_view(
        openapi.Info(
            title="kuttuktoo API",
            default_version="v1",
            description="API документация",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    *(
        [
            re_path(r"^api/swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
            path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
            path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
        ]
        if get_schema_view is not None
        else []
    ),
    path("api/", include("offers.urls")),

    # Главная (Vite dist index.html)
    path("", spa_view),
]

# SPA fallback (React Router refresh)
urlpatterns += [
    re_path(r"^(?!api/|admin/|static/|media/).*$", spa_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
