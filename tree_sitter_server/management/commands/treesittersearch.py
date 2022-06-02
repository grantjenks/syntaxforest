"""Syntax Forest Search
"""

import functools
import logging
import operator
import time

import modelqueue
import tree_sitter_languages as ts

from django.core.management.base import BaseCommand
from django.db.models import Q

from ...models import Capture, Result, Search, Source

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syntax Forest Search'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        while True:
            searches = Search.objects.all()
            search = modelqueue.run(searches, 'status', self.process)
            if search is None:
                log.info('Nothing to search')
                time.sleep(1)

    def process(self, search):
        log.info(f'Processing {search}')
        Result.objects.filter(search=search).delete()
        sources = Source.objects.filter(language=search.language)
        language = ts.get_language(search.language)
        parser = ts.get_parser(search.language)
        query = language.query(search.query)

        for source in sources:
            tree = parser.parse(source.text.encode())
            node = tree.root_node
            captures = query.captures(node)

            if not captures:
                continue

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
