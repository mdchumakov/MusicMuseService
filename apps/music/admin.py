from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.music import models


@admin.register(models.Artists)
class ArtistsAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "description", "is_verified", "created")
    # По каким полям можно искать в панели
    search_fields = (
        "id",
        "slug",
        "name",
        "avatar__name",
    )

    # Фильтры в боковой панели
    list_filter = ("is_verified",)
    # Предварительное заполнение slug на основе name
    # (актуально, если slug делается по названию)
    prepopulated_fields = {"slug": ("name",)}

    # Отображение дат в иерархическом виде (по дате создания)
    date_hierarchy = "created"

    # Сортировка по умолчанию
    ordering = ("-created",)

    filter_horizontal = ("genres",)

    # Поля, которые будут отображаться и доступны для редактирования
    # при редактировании записи (можно разбивать на группы)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "label",
                    "genres",
                    "gender",
                    "is_verified",
                    "avatar",
                    "preview",
                ),
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": (
                    "bio",
                    "birth_date",
                    "country",
                ),
                "classes": ("collapse",),  # позволяет сворачивать блок
            },
        ),
        (
            "Служебные поля",
            {
                "fields": (
                    "created",
                    "updated",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Поля, которые нельзя редактировать (readonly)
    readonly_fields = ("preview", "created", "updated")

    @staticmethod
    def preview(obj) -> str:
        return mark_safe(f'<img src="{obj.avatar.image.url}" style="max-height: 200px;"/>')


@admin.register(models.Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "sound_display", "name", "created")
    readonly_fields = ("sound_display",)
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)

    def sound_display(self, item) -> str:
        if item.audio:
            return mark_safe(f'<audio controls name="media"><source src="{item.audio.url}" type="audio/mpeg"></audio>')
        return ""

    sound_display.short_description = "Трек"
    sound_display.allow_tags = True


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "video", "created")
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)


@admin.register(models.Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "parent", "description", "created")
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "icon", "name", "image", "created")
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)

    def icon(self, item) -> str:
        return mark_safe(f'<img src="{item.image.url}" style="max-height: 20px;"/>')

    icon.short_description = "Изображение"
    icon.allow_tags = True


@admin.register(models.Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "description", "created")
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Releases)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "name",
        "icon",
        "status",
        "release_type",
        "release_date",
        "publication_time",
    )
    search_fields = ("id", "name",)
    date_hierarchy = "created"
    ordering = ("-created",)
    filter_horizontal = ("genres", "artists")

    def icon(self, item) -> str:
        return mark_safe(f'<img src="{item.cover_image.image.url}" style="max-height: 20px;"/>')

    @staticmethod
    def preview(obj) -> str:
        return mark_safe(f'<img src="{obj.cover_image.image.url}" style="max-height: 200px;"/>')

    icon.short_description = "Обложка"
    icon.allow_tags = True


@admin.register(models.Tracks)
class TracksAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "name",
        "sound_display",
        "status",
        "track_type",
        "age_related_content",
        "release_date",
        "publication_time",
    )
    search_fields = ("id", "name",)
    filter_horizontal = ("genres", "artists")

    def sound_display(self, item) -> str:
        return mark_safe(
            f'<audio controls name="media"><source src="{item.track.audio.url}" type="audio/mpeg"></audio>'
        )

    sound_display.short_description = "Трек"
    sound_display.allow_tags = True
