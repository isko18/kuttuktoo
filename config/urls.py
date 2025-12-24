from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

spa_view = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
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
