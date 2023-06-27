"""Syntax Forest Task Processor
"""

import logging
import time

import modelqueue
import tree_sitter_languages as ts
from django.core.management.base import BaseCommand
from django.db.models import F

from ...models import Capture, Result, Search, Source, Task

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syntax Forest Task Processor'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        while True:
            tasks = Task.objects.all()
            task = modelqueue.run(tasks, 'status', self.process)
            if task is None:
                log.info('No tasks to process')
                time.sleep(1)

    def process(self, task):
        log.info(f'Processing {task}')
        search = task.search
        language = ts.get_language(search.language)
        query = language.query(search.query)
        source = task.source
        parser = ts.get_parser(search.language)
        tree = parser.parse(source.text.encode())
        node = tree.root_node
        captures = query.captures(node)

        if not captures:
            return

        result = Result(
            search=search,
            path=source.path,
            sha=source.sha,
            text=source.text,
            language=source.language,
        )
        result.save()
        db_captures = []

        for node, name in captures:
            start_point_row, start_point_col = node.start_point
            end_point_row, end_point_col = node.end_point
            db_capture = Capture(
                result=result,
                name=name,
                start_byte=node.start_byte,
                end_byte=node.end_byte,
                start_point_line=start_point_row + 1,
                start_point_col=start_point_col,
                end_point_line=end_point_row + 1,
                end_point_col=end_point_col,
            )
            db_captures.append(db_capture)

        Capture.objects.bulk_create(db_captures)

        search.search_count = F('search_count') + 1
        search.save()
