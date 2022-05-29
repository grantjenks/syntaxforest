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
    progress = models.FloatField(default=0)

    def get_ref(self):
        return self.name or f'Search #{self.id}'

    def __str__(self):
        return f'Search({self.query!r})'


class Source(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    path = models.CharField(unique=True, max_length=4096)
    sha = models.CharField(blank=True, max_length=100)
    text = models.TextField(blank=True)
    language = models.CharField(max_length=100)

    def __str__(self):
        return f'Source({self.path!r})'


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    path = models.CharField(max_length=4096)
    sha = models.CharField(blank=True, max_length=100)
    text = models.TextField(blank=True)
    language = models.CharField(max_length=100)


class Capture(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_byte = models.BigIntegerField()
    end_byte = models.BigIntegerField()
    start_point_line = models.BigIntegerField()
    start_point_col = models.BigIntegerField()
    end_point_line = models.BigIntegerField()
    end_point_col = models.BigIntegerField()
