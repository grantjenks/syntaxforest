from django.contrib import admin
from .models import Search, Source, Result, Capture, Task


class SearchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Search, SearchAdmin)


class SourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Source, SourceAdmin)


class ResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Result, ResultAdmin)


class CaptureAdmin(admin.ModelAdmin):
    pass


admin.site.register(Capture, CaptureAdmin)


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
