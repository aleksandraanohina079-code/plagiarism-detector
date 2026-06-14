import json
from django.shortcuts import render
from django import forms
from .utils import detector, clean_text, get_text_stats, get_keywords, analyze_sentiment, generate_wordcloud
from .file_utils import extract_text_from_file
from core.models import CorpusDocument, CheckHistory

class TextCheckForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'class': 'form-control', 'placeholder': 'Введите текст для проверки...'}),
        label="Текст для проверки",
        required=False
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.txt,.docx,.pdf'}),
        label="Или загрузите файл",
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        file = cleaned_data.get('file')
        
        if not text and not file:
            raise forms.ValidationError('Введите текст или загрузите файл')
        return cleaned_data

def index(request):
    return render(request, 'analyzer/index.html', {
        'form': TextCheckForm(),
        'total_docs': CorpusDocument.objects.count()
    })

def check_text(request):
    if request.method == 'POST':
        form = TextCheckForm(request.POST, request.FILES)
        if form.is_valid():
            user_text = form.cleaned_data.get('text', '')
            uploaded_file = request.FILES.get('file')
            
            if uploaded_file:
                user_text = extract_text_from_file(uploaded_file)
                if not user_text:
                    return render(request, 'analyzer/index.html', {
                        'form': form,
                        'error': 'Не удалось прочитать файл. Поддерживаются: TXT, DOCX, PDF',
                        'total_docs': CorpusDocument.objects.count()
                    })
            
            if not user_text or not user_text.strip():
                return render(request, 'analyzer/index.html', {
                    'form': form,
                    'error': 'Текст не может быть пустым',
                    'total_docs': CorpusDocument.objects.count()
                })
            
            # 1. Статистика текста
            stats = get_text_stats(user_text)
            
            # 2. Ключевые слова
            keywords = get_keywords(user_text)
            
            # 3. Анализ тональности
            sentiment = analyze_sentiment(user_text)
            
            # 4. Облако слов
            wordcloud_img = generate_wordcloud(user_text)
            
            # 5. Поиск заимствований
            results = []
            for doc in CorpusDocument.objects.all():
                sim = detector.compute_similarity(clean_text(user_text), clean_text(doc.content))
                if sim >= 0.2:
                    results.append({
                        'id': doc.id,
                        'title': doc.title,
                        'similarity': round(sim * 100, 1),
                        'snippets': detector.find_common_snippets(clean_text(user_text), clean_text(doc.content))[:3],
                    })
            results.sort(key=lambda x: x['similarity'], reverse=True)
            uniqueness = 100 - (results[0]['similarity'] if results else 0)
            
            # Сохраняем в историю
            CheckHistory.objects.create(
                text_checked=user_text[:500],
                uniqueness_score=uniqueness,
                matched_count=len(results),
                keywords=', '.join(keywords[:10]),
                stats=json.dumps(stats, ensure_ascii=False)
            )
            
            history = CheckHistory.objects.all().order_by('-created_at')[:5]
            
            return render(request, 'analyzer/result.html', {
                'original_text': user_text,
                'results': results,
                'uniqueness': round(uniqueness, 1),
                'total_checked': CorpusDocument.objects.count(),
                'stats': stats,
                'keywords': keywords,
                'sentiment': sentiment,
                'wordcloud_img': wordcloud_img,
                'history': history,
                'filename': uploaded_file.name if uploaded_file else None
            })
    
    return render(request, 'analyzer/index.html', {'form': TextCheckForm(), 'total_docs': CorpusDocument.objects.count()})

def history(request):
    all_history = CheckHistory.objects.all().order_by('-created_at')
    return render(request, 'analyzer/history.html', {'history': all_history})
