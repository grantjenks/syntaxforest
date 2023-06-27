"""Syntax Forest Search Processor
"""

import logging
import time

import modelqueue
from django.core.management.base import BaseCommand

from ...models import Capture, Result, Search, Source, Task

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syntax Forest Search Processor'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        while True:
            searches = Search.objects.all()
            search = modelqueue.run(searches, 'status', self.process)
            if search is None:
                log.info('No searches to process')
                time.sleep(1)

    def process(self, search):
        log.info(f'Processing {search}')
        Result.objects.filter(search=search).delete()
        chunk_size = 1000
        sources = (
            Source.objects.filter(language=search.language)
            .only('id')
            .iterator(chunk_size=chunk_size)
        )
        tasks = []
        start_priority = modelqueue.Status.waiting().priority

        for index, source in enumerate(sources):
            status = modelqueue.Status.waiting(priority=start_priority + index)
            task = Task(
                search=search,
                source=source,
                status=status,
            )
            tasks.append(task)

            if len(tasks) >= chunk_size:
                log.info(f'Creating tasks {index + 1}')
                Task.objects.bulk_create(tasks)
                tasks = []

        log.info(f'Creating tasks {index + 1}')
        Task.objects.bulk_create(tasks)

        search.source_count = index + 1
        search.save()
