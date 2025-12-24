from django.db import models


class SiteSettings(models.Model):
    brand_name = models.CharField(
        max_length=80,
        default="kuttuktoo",
        blank=True,
        verbose_name="Название бренда",
    )
    subtitle = models.CharField(
        max_length=120,
        default="видео + тарифтер",
        blank=True,
        verbose_name="Подзаголовок",
    )
    whatsapp_link = models.URLField(
        default="https://wa.me/996221000953",
        blank=True,
        verbose_name="Ссылка WhatsApp",
    )
    footer_text = models.CharField(
        max_length=120,
        default="© REKLAM",
        blank=True,
        verbose_name="Текст в футере",
    )

    logo = models.ImageField(
        upload_to="site/logo/",
        null=True,
        blank=True,
        verbose_name="Логотип",
    )

    def __str__(self):
        return "Настройки сайта"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"


class Offer(models.Model):
    key = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name="Ключ (slug)",
        help_text="Уникальный ключ тарифа, например: econom, standard, invite",
    )
    title = models.CharField(
        max_length=120,
        verbose_name="Название тарифа",
    )
    sub = models.CharField(
        max_length=180,
        blank=True,
        verbose_name="Подзаголовок",
    )
    badge = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Бейдж (лейбл)",
        help_text="Например: VIP, Көп алынат, Сунуштайм",
    )
    price = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Цена",
        help_text='Например: "2 000 сом"',
    )
    wa_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Текст для WhatsApp",
        help_text="Сообщение, которое уйдет в WhatsApp при нажатии «Заказ берүү»",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    def __str__(self):
        return f"{self.title} ({self.key})"

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class OfferFeature(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Тариф",
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Текст пункта",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Пункт тарифа"
        verbose_name_plural = "Пункты тарифа"

    def __str__(self):
        return f"{self.offer.key}: {self.text}"


class OfferVideo(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Тариф",
    )
    file = models.FileField(
        upload_to="offers/videos/",
        verbose_name="Видео файл",
    )
    duration = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Длительность",
        help_text='Например: "0:56"',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Видео тарифа"
        verbose_name_plural = "Видео тарифов"

    def __str__(self):
        return f"{self.offer.key}: video#{self.id}"