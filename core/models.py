from django.db import models

class CorpusDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class CheckHistory(models.Model):
    text_checked = models.TextField()
    uniqueness_score = models.FloatField()
    matched_count = models.IntegerField(default=0)
    keywords = models.TextField(blank=True, default='')
    stats = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Проверка от {self.created_at.strftime('%d.%m.%Y %H:%M')}"
