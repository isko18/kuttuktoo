from rest_framework import generics, permissions
from .models import SiteSettings, Offer
from .serializers import SiteSettingsSerializer, OfferPublicSerializer


class SiteSettingsView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        obj, _ = SiteSettings.objects.get_or_create(id=1)
        return obj


class OfferListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferPublicSerializer

    def get_queryset(self):
        return (
            Offer.objects.filter(is_active=True)
            .prefetch_related("videos", "features")
            .order_by("sort_order", "id")
        )
