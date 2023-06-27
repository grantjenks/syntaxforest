"""Syntax Forest Import

python manage.py syntaxforestimport --prefix github.com/python/cpython/v3.11.4/
"""

import logging
import os
import pathlib
import time
import tqdm

import modelqueue
from django.core.management.base import BaseCommand

from ...models import Source

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Syntax Forest Import'

    def add_arguments(self, parser):
        parser.add_argument('--prefix')
        parser.add_argument('--directory', default='.')
        parser.add_argument('--glob', default='**/*.py')
        parser.add_argument('--language', default='python')

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        prefix = options['prefix']
        directory = options['directory']
        glob = options['glob']
        language = options['language']
        os.chdir(directory)
        dir_path = pathlib.Path()
        py_paths = dir_path.glob(glob)

        for py_path in tqdm.tqdm(py_paths):
            try:
                text = py_path.read_text()
            except UnicodeDecodeError:
                continue
            path = prefix + str(py_path)
            source = Source(
                path=path,
                text=text,
                language=language,
            )
            source.save()
