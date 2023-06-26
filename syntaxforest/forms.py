import tree_sitter_languages as ts

from django.forms import ModelForm, ValidationError

from .models import LANGUAGES, Search, Source


class SearchForm(ModelForm):
    def clean_language(self):
        language = self.cleaned_data.get('language', '')
        print(language)
        if language not in LANGUAGES:
            raise ValidationError('unsupported language')
        return language

    def clean(self):
        super().clean()
        language_name = self.cleaned_data.get('language')
        query_text = self.cleaned_data.get('query')
        try:
            language = ts.get_language(language_name)
            query = language.query(query_text)
        except Exception as exc:
            raise ValidationError(str(exc))

    class Meta:
        model = Search
        fields = ['query', 'name', 'language']


class SourceForm(ModelForm):
    def validate_unique(self):
        # Skip unique field validation.
        pass

    class Meta:
        model = Source
        fields = ['sha', 'path', 'text', 'language']
