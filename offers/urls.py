from django.urls import path
from .views import SiteSettingsView, OfferListView

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("offers/", OfferListView.as_view(), name="offers-list"),
]
