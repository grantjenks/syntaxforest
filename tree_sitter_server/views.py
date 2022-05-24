import modelqueue

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
        return render(request, 'tree_sitter_server/source.html', {'source': source})
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save()
            return redirect('source', path=source.path)
    else:
        form = SourceForm()
    return render(request, 'tree_sitter_server/source.html', {'form': form})
