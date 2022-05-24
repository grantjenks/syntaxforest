import modelqueue

from django.db import models


class Source(models.Model):
    path = models.TextField(unique=True)
    source = models.TextField()

    def __str__(self):
        return f'Source({self.path!r})'


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
