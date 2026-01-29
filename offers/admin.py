from django.contrib import admin
from .models import SiteSettings, Offer, OfferFeature, OfferVideo, OfferDeviceVideo


class OfferFeatureInline(admin.TabularInline):
    model = OfferFeature
    extra = 0


class OfferVideoInline(admin.TabularInline):
    model = OfferVideo
    extra = 0
    fields = ("file", "duration", "sort_order")


class OfferDeviceVideoInline(admin.TabularInline):
    model = OfferDeviceVideo
    extra = 0
    fields = ("desktop_file", "mobile_file", "duration", "sort_order")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "price", "badge", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("key", "title")
    inlines = [OfferDeviceVideoInline, OfferVideoInline, OfferFeatureInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "subtitle", "whatsapp_link", "footer_text")


@admin.register(OfferDeviceVideo)
class OfferDeviceVideoAdmin(admin.ModelAdmin):
    list_display = ("offer", "id", "sort_order", "duration")
    list_filter = ("offer",)
    search_fields = ("offer__key", "offer__title")
    ordering = ("offer__sort_order", "offer__id", "sort_order", "id")
