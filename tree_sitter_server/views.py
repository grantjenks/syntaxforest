from django.shortcuts import get_object_or_404, redirect, render

from .forms import SearchForm
from .models import Search


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
    return render(request, 'tree_sitter_server/search.html', {'search': search})
