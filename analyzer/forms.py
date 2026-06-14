from django import forms

class TextCheckForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите текст для проверки...'}),
        label="Текст для проверки"
    )
