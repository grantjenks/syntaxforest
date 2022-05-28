import modelqueue

from django.db import models


class Search(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(blank=True, default='', max_length=100)
    language = models.CharField(max_length=100)
    query = models.TextField()
    status = modelqueue.StatusField(
        db_index=True,
        default=modelqueue.Status.waiting,
    )

    def get_ref(self):
        return self.name or f'Search #{self.id}'

    def __str__(self):
        return f'Search({self.query!r})'


class Source(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    sha = models.CharField(blank=True, max_length=100)
    path = models.CharField(unique=True, max_length=4096)
    text = models.TextField(blank=True)
    language = models.CharField(max_length=100)

    def __str__(self):
        return f'Source({self.path!r})'


class Capture(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=4096)
    sha = models.CharField(blank=True, max_length=100)
