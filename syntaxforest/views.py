import modelqueue
import tree_sitter_languages as ts
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SearchForm, SourceForm
from .models import Search, Source, Capture

EXTENSIONS = {'py': 'python', 'java': 'java'}


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save()
            return redirect('search', search_id=search.id)
    else:
        form = SearchForm()
    searches = Search.objects.order_by('-create_time')[:10]
    return render(
        request,
        'syntaxforest/index.html',
        {'searches': searches, 'form': form},
    )


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
    try:
        offset = int(request.GET.get('offset', 0))
    except Exception:
        offset = 0
    results = search.result_set.all()
    captures = Capture.objects.filter(result__in=results).order_by('id')
    paginator = Paginator(captures, 25)
    page_num = request.GET.get("page")
    page = paginator.get_page(page_num)
    page_range = paginator.get_elided_page_range(page.number)
    return render(
        request,
        'syntaxforest/search.html',
        {
            'search': search,
            'page': page,
            'paginator': paginator,
            'page_range': page_range,
        },
    )


def source(request, path):
    if path != '':
        return source_path(request, path)
    return source_form(request, path)


def source_path(request, path):
    source = get_object_or_404(Source, path=path)
    code, style = source.to_html()
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
    return render(request, 'syntaxforest/source-path.html', context)


def source_form(request, path):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            if source.language == 'language':
                extension = source.path.split('.')[-1]
                language = EXTENSIONS[extension]
                source.language = language
            with transaction.atomic():
                Source.objects.filter(path=source.path).delete()
                source.save()
            return redirect('source', path=source.path)
    else:
        form = SourceForm()
    sources = Source.objects.order_by('-update_time')[:10]
    context = {'form': form, 'sources': sources}
    return render(request, 'syntaxforest/source-form.html', context)
