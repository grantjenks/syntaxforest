import modelqueue
import tree_sitter_languages as ts

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

from django.shortcuts import get_object_or_404, redirect, render

from .forms import SearchForm, SourceForm
from .models import Search, Source


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save()
            return redirect('search', search_id=search.id)
    else:
        form = SearchForm()
    searches = Search.objects.order_by('-create_time')[:10]
    return render(request, 'tree_sitter_server/index.html', {'searches': searches})


def search(request, search_id):
    search = get_object_or_404(Search, pk=search_id)
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'rerun':
            search.status = modelqueue.Status.waiting()
            search.save()
            return redirect('search', search_id=search.id)
        else:
            assert action == 'delete'
            search.delete()
            return redirect('index')
    return render(request, 'tree_sitter_server/search.html', {'search': search})


def source(request, path):
    if path != '':
        source = get_object_or_404(Source, path=path)
        lexer = get_lexer_for_filename(path)
        formatter = HtmlFormatter(
            linenos=True,
            lineanchors='line',
            anchorlinenos=True,
        )
        code = highlight(source.text, lexer, formatter)
        style = formatter.get_style_defs()
        parser = ts.get_parser('python')
        tree = parser.parse(source.text.encode())
        node = tree.root_node
        sexp = node.sexp()
        parts = sexp.split()
        indent = 0
        for index in range(len(parts)):
            part = parts[index]
            parts[index] = ' ' * (indent * 2) + part
            indent += part.count('(') - part.count(')')
        sexp = '\n'.join(parts)
        context = {'source': source, 'code': code, 'style': style, 'sexp': sexp}
        return render(request, 'tree_sitter_server/source.html', context)

    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save()
            return redirect('source', path=source.path)
    else:
        form = SourceForm()
    sources = Source.objects.order_by('-update_time')[:10]
    context = {'form': form, 'sources': sources}
    return render(request, 'tree_sitter_server/source.html', context)
