# Generated by Django 5.1.2 on 2024-11-03 20:33

import django_countries.fields
import pictures.models
from django.db import migrations

import music.models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0002_albums_description_genres_image_tracks_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="albums",
            name="cover_image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_albums_to,
                verbose_name="Ссылка на изображение",
                width_field=1200,
            ),
        ),
        migrations.AlterField(
            model_name="artists",
            name="avatar_url",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_artists_to,
                verbose_name="Ссылка на аватар",
                width_field=1200,
            ),
        ),
        migrations.AlterField(
            model_name="artists",
            name="country",
            field=django_countries.fields.CountryField(default="RU", max_length=2, verbose_name="Страна"),
        ),
        migrations.AlterField(
            model_name="generatedimagecontent",
            name="image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_images_to,
                verbose_name="Ссылка на сгенерированное изображение",
                width_field=1200,
            ),
        ),
        migrations.AlterField(
            model_name="genres",
            name="image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                default=None,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_genres_to,
                verbose_name="Ссылка на изображение жанра",
                width_field=1200,
            ),
        ),
        migrations.AlterField(
            model_name="labels",
            name="cover_image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_labels_to,
                verbose_name="Ссылка на изображение",
                width_field=1200,
            ),
        ),
        migrations.AlterField(
            model_name="tracks",
            name="cover_image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                file_types=["WEBP"],
                grid_columns=12,
                height_field=1080,
                pixel_densities=[1, 2],
                storage=music.models._get_public_media_storage,
                upload_to=music.models._upload_tracks_to,
                verbose_name="Ссылка на изображение",
                width_field=1200,
            ),
        ),
    ]
