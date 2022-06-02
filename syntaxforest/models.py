import modelqueue

from lxml import etree

from pygments import highlight
from pygments.lexers import TextLexer, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound as PygmentsClassNotFound

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

    def to_html(self, lines=None):
        try:
            lexer = get_lexer_for_filename(self.path)
        except PygmentsClassNotFound:
            lexer = TextLexer()

        formatter = HtmlFormatter(
            anchorlinenos=True,
            lineanchors='line',
            linenos=True,
            linespans='row',
            wrapcode=True,
        )
        code = highlight(self.text, lexer, formatter)

        if lines is not None:
            tree = etree.fromstring(code)

            # Keep only spans containing source rows from lines.

            rows = tree.xpath('//span[@id]')
            keep_rows = {f'row-{line}' for line in lines}
            for row in rows:
                if row.get('id') not in keep_rows:
                    row.getparent().remove(row)

            # Keep only spans containing line number anchors from lines.

            linenos = tree.xpath('//a[@href]')
            linenos = [
                anchor for anchor in linenos
                if anchor.get('href').startswith('#line-')
            ]
            keep_lines = {f'#line-{line}' for line in lines}

            for lineno in linenos:
                if lineno.get('href') not in keep_lines:
                    span = lineno.getparent()
                    span.getparent().remove(span)

            code = etree.tostring(tree, encoding='unicode')

        style = formatter.get_style_defs()
        return code, style

    def __str__(self):
        return f'Source({self.path!r})'


class Result(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    path = models.CharField(max_length=4096)
    sha = models.CharField(blank=True, max_length=100)
    text = models.TextField(blank=True)
    language = models.CharField(max_length=100)

    to_html = Source.to_html


class Capture(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_byte = models.BigIntegerField()
    end_byte = models.BigIntegerField()
    start_point_line = models.BigIntegerField()
    start_point_col = models.BigIntegerField()
    end_point_line = models.BigIntegerField()
    end_point_col = models.BigIntegerField()

    def to_html(self):
        lines = range(self.start_point_line, self.end_point_line + 1)
        return self.result.to_html(lines)
