from django import forms


class TextCheckForm(forms.Form):
    """
    Форма для ввода текста или загрузки файла.

    Поля:
        text (str): Текст для проверки
        file (File): Загруженный файл
    """

    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'class': 'form-control',
            'placeholder': 'Введите текст для проверки...'
        }),
        label="Текст для проверки",
        required=False
    )

    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.txt,.docx,.pdf'
        }),
        label="Или загрузите файл",
        required=False
    )

    def clean(self):
        """
        Проверяет, что передан либо текст, либо файл.

        Returns:
            dict: Очищенные данные

        Raises:
            ValidationError: Если текст и файл пусты
        """
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        file = cleaned_data.get('file')

        if not text and not file:
            raise forms.ValidationError('Введите текст или загрузите файл')
        return cleaned_data
