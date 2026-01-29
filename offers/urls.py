from django.urls import path
from .views import SiteSettingsView, OfferListView, OfferDeviceVideoListView

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("offers/", OfferListView.as_view(), name="offers-list"),
    path("offers/<slug:key>/videos/", OfferDeviceVideoListView.as_view(), name="offer-device-videos"),
    path("offers/videos/", OfferDeviceVideoListView.as_view(), name="offer-device-videos-all"),
]
