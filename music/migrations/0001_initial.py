# Generated by Django 5.1.1 on 2024-09-08 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.CharField(verbose_name='Описание')),
            ],
            options={
                'abstract': False,
                'indexes': [models.Index(fields=['name', '-created', '-updated'], name='music_genre_name_788914_idx')],
            },
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.CharField(verbose_name='Описание')),
                ('cover_image', models.ImageField(upload_to='', verbose_name='Ссылка на изображение')),
            ],
            options={
                'abstract': False,
                'indexes': [models.Index(fields=['name', '-created', '-updated'], name='music_label_name_b5ef76_idx')],
            },
        ),
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.CharField(verbose_name='Описание')),
                ('bio', models.TextField(verbose_name='Биография')),
                ('avatar_url', models.ImageField(upload_to='', verbose_name='Ссылка на аватар')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('country', models.CharField(verbose_name='Страна')),
                ('genres', models.ManyToManyField(to='music.genres', verbose_name='Жанры')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.labels', verbose_name='Лейбл')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Albums',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('cover_image', models.ImageField(upload_to='', verbose_name='Ссылка на изображение')),
                ('release_date', models.DateField(verbose_name='Дата выхода')),
                ('artists', models.ManyToManyField(to='music.artists', verbose_name='Исполнители')),
                ('genres', models.ManyToManyField(to='music.genres', verbose_name='Жанры')),
                ('labels', models.ManyToManyField(to='music.labels', verbose_name='Лейблы')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('cover_image', models.ImageField(upload_to='', verbose_name='Ссылка на изображение')),
                ('track', models.FileField(upload_to='', verbose_name='Ссылка на трек')),
                ('duration', models.DurationField(verbose_name='Длительность')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.albums', verbose_name='Альбом')),
                ('artists', models.ManyToManyField(to='music.artists', verbose_name='Исполнители')),
                ('genres', models.ManyToManyField(to='music.genres', verbose_name='Жанры')),
                ('label', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='music.labels', verbose_name='Лейбл')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='artists',
            index=models.Index(fields=['name', '-created', '-updated'], name='music_artis_name_87e857_idx'),
        ),
        migrations.AddIndex(
            model_name='albums',
            index=models.Index(fields=['name', '-created', '-updated'], name='music_album_name_6865eb_idx'),
        ),
        migrations.AddIndex(
            model_name='tracks',
            index=models.Index(fields=['name', '-created', '-updated'], name='music_track_name_76869a_idx'),
        ),
    ]
