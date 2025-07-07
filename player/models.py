import os
import pathlib

from django.db import models

from main import settings


def cover_image_path(instance, filename):
    path = f'{instance.name}/{filename}'
    return path


def file_path(instance, filename):
    path = f'{instance.name}/{filename}'
    return path


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    duration = models.IntegerField()
    cover_image = models.ImageField(upload_to=cover_image_path, default='default.png', blank=True, null=True)
    file = models.FileField(upload_to=file_path)

    def delete(self, *args, **kwargs):
        storage, path = self.cover_image.storage, self.cover_image.path
        storage.delete(path)
        storage, path = self.file.storage,self.file.path
        storage.delete(path)
        os.rmdir(f'media\\{self.name}')
        super().delete(*args, **kwargs)
