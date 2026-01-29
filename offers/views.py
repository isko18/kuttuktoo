from rest_framework import generics, permissions
from .models import SiteSettings, Offer, OfferDeviceVideo
from .serializers import SiteSettingsSerializer, OfferPublicSerializer, OfferDeviceVideoSerializer


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


class OfferDeviceVideoListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferDeviceVideoSerializer

    def get_queryset(self):
        key = self.kwargs.get("key")
        qs = OfferDeviceVideo.objects.select_related("offer").order_by("sort_order", "id")
        if key:
            qs = qs.filter(offer__key=key)
        return qs
