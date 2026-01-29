from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )
except Exception:
    SpectacularAPIView = None
    SpectacularSwaggerView = None
    SpectacularRedocView = None

spa_view = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    *(
        [
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
            path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
        ]
        if SpectacularAPIView is not None
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
