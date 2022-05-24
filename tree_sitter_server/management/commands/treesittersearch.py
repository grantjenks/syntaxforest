import functools
import logging
import operator
import time

import modelqueue
import tree_sitter_languages as ts

from django.core.management.base import BaseCommand
from django.db.models import Q

from ...models import Capture, Search, Source

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Execute Tree-sitter Search'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        while True:
            searches = Search.objects.all()
            search = modelqueue.run(searches, 'status', self.process)
            if search is None:
                time.sleep(1)

    def process(self, search):
        log.info(f'Processing {search}')
        extensions_map = {
            'python': ['.py'],
        }
        extensions = extensions_map[search.language]
        filters = [Q(path__endswith=extension) for extension in extensions]
        querymap_filter = functools.reduce(operator.or_, filters, Q())
        sources = Source.objects.filter(querymap_filter)
        language = ts.get_language(search.language)
        parser = ts.get_parser(search.language)
        query = language.query(search.query)
        for source in sources:
            tree = parser.parse(source.text.encode())
            node = tree.root_node
            captures = query.captures(node)
            for capture in captures:
                print(capture)
