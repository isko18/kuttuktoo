from django.contrib import admin
from .models import SiteSettings, Offer, OfferFeature, OfferVideo


class OfferFeatureInline(admin.TabularInline):
    model = OfferFeature
    extra = 0


class OfferVideoInline(admin.TabularInline):
    model = OfferVideo
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "price", "badge", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("key", "title")
    inlines = [OfferVideoInline, OfferFeatureInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "subtitle", "whatsapp_link", "footer_text")
