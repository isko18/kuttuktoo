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
            .select_related("device_video")
            .prefetch_related("videos", "features")
            .order_by("sort_order", "id")
        )


class OfferDeviceVideoListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferDeviceVideoSerializer

    def get_queryset(self):
        key = self.kwargs.get("key")
        qs = OfferDeviceVideo.objects.all().order_by("id")
        if not key:
            return qs

        try:
            offer = Offer.objects.select_related("device_video").only("id", "device_video").get(key=key)
        except Offer.DoesNotExist:
            return qs.none()

        if not offer.device_video_id:
            return qs.none()
        return qs.filter(id=offer.device_video_id)
