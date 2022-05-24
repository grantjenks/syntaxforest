import modelqueue

from django.core.management.base import BaseCommand

from ...models import Search


class Command(BaseCommand):
    help = 'Execute Tree-sitter Search'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        while True:
            searches = Search.objects.all()
            search = modelqueue.run(searches, 'status', self.process)
            if search is None:
                time.sleep(1)

    def process(self, search):
        pass
