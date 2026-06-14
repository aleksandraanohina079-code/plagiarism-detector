from django.contrib import admin
from .models import CorpusDocument, CheckHistory

@admin.register(CorpusDocument)
class CorpusDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']

@admin.register(CheckHistory)
class CheckHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'uniqueness_score', 'created_at']
