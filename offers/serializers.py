from rest_framework import serializers
from .models import SiteSettings, Offer, OfferDeviceVideo


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = ("brand_name", "subtitle", "whatsapp_link", "footer_text", "logo_url")

    def get_logo_url(self, obj):
        try:
            if not obj.logo:
                return ""
            req = self.context.get("request")
            url = obj.logo.url
            return req.build_absolute_uri(url) if req else url
        except Exception:
            return ""


class OfferPublicSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    list = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ("key", "title", "sub", "badge", "price", "wa_text", "sort_order", "videos", "list")

    def get_videos(self, obj):
        req = self.context.get("request")

        def _build(file_field):
            try:
                if not file_field:
                    return ""
                url = file_field.url
                return req.build_absolute_uri(url) if req else url
            except Exception:
                return ""

        out = []

        device_qs = getattr(obj, "device_videos", None)
        device_items = device_qs.all().order_by("sort_order", "id") if device_qs is not None else []
        for v in device_items:
            mobile_src = _build(v.mobile_file)
            desktop_src = _build(v.desktop_file)
            out.append(
                {
                    "id": v.id,
                    "src": desktop_src or mobile_src or "",
                    "mobile_src": mobile_src,
                    "desktop_src": desktop_src,
                    "duration": v.duration or "",
                }
            )

        if not out:  # fallback to старые OfferVideo
            for v in obj.videos.all().order_by("sort_order", "id"):
                src = _build(v.file)
                out.append(
                    {
                        "id": v.id,
                        "src": src or "",
                        "mobile_src": "",
                        "desktop_src": src or "",
                        "duration": v.duration or "",
                    }
                )

        return out

    def get_list(self, obj):
        return [f.text for f in obj.features.all().order_by("sort_order", "id")]


class OfferDeviceVideoSerializer(serializers.ModelSerializer):
    mobile_src = serializers.SerializerMethodField()
    desktop_src = serializers.SerializerMethodField()
    src = serializers.SerializerMethodField()

    class Meta:
        model = OfferDeviceVideo
        fields = ("id", "src", "mobile_src", "desktop_src", "duration", "sort_order")

    def _build(self, file_field):
        try:
            if not file_field:
                return ""
            req = self.context.get("request")
            url = file_field.url
            return req.build_absolute_uri(url) if req else url
        except Exception:
            return ""

    def get_mobile_src(self, obj):
        return self._build(obj.mobile_file)

    def get_desktop_src(self, obj):
        return self._build(obj.desktop_file)

    def get_src(self, obj):
        return self.get_desktop_src(obj) or self.get_mobile_src(obj)
