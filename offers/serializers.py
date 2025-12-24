from rest_framework import serializers
from .models import SiteSettings, Offer


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
        out = []
        for v in obj.videos.all().order_by("sort_order", "id"):
            try:
                url = v.file.url
                src = req.build_absolute_uri(url) if req else url
            except Exception:
                src = ""
            out.append(
                {
                    "id": v.id,
                    "src": src,
                    "duration": v.duration or "",
                }
            )
        return out

    def get_list(self, obj):
        return [f.text for f in obj.features.all().order_by("sort_order", "id")]
