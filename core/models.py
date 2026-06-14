from django.db import models


class CorpusDocument(models.Model):
    """
    Модель для хранения документов в корпусе.

    Поля:
        title (str): Название документа
        content (str): Текст документа
        file_name (str): Имя загруженного файла
        created_at (datetime): Дата добавления
    """

    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(verbose_name="Содержимое")
    file_name = models.CharField(max_length=255, blank=True, verbose_name="Имя файла")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Документ корпуса"
        verbose_name_plural = "Документы корпуса"
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Возвращает название документа."""
        return self.title


class CheckHistory(models.Model):
    """
    Модель для хранения истории проверок.

    Поля:
        text_checked (str): Проверенный текст
        uniqueness_score (float): Процент уникальности
        matched_count (int): Количество совпадений
        keywords (str): Ключевые слова
        stats (str): Статистика в JSON
        created_at (datetime): Дата проверки
    """

    text_checked = models.TextField(verbose_name="Проверенный текст")
    uniqueness_score = models.FloatField(verbose_name="Уникальность (%)")
    matched_count = models.IntegerField(default=0, verbose_name="Количество совпадений")
    keywords = models.TextField(blank=True, default='', verbose_name="Ключевые слова")
    stats = models.TextField(blank=True, default='', verbose_name="Статистика")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проверки")

    class Meta:
        verbose_name = "История проверки"
        verbose_name_plural = "История проверок"
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Возвращает строковое представление проверки."""
        return f"Проверка от {self.created_at.strftime('%d.%m.%Y %H:%M')}"
