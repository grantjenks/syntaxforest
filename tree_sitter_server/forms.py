from django.forms import ModelForm

from .models import Search, Source


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ['query', 'name', 'language']


class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ['sha', 'path', 'text']
