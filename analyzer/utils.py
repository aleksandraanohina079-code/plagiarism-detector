import ssl
import nltk
import re
import io
import base64
import os
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from typing import Set, List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

from .sentiment_analyzer import analyze_sentiment_simple

# Отключаем проверку SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Устанавливаем Agg бэкенд для matplotlib
matplotlib.use('Agg')

# NLTK настройки
nltk.data.path.append(os.path.expanduser('~/nltk_data'))

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


def clean_text(text: str) -> str:
    """Очищает текст от лишних символов."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_ngrams(text: str, n: int = 4) -> Set[str]:
    """Разбивает текст на n-граммы."""
    words = nltk.word_tokenize(text)
    if len(words) < n:
        return set()
    ngrams = []
    for i in range(len(words) - n + 1):
        ngrams.append(' '.join(words[i:i + n]))
    return set(ngrams)


def get_text_stats(text: str) -> dict:
    """Подсчитывает статистику текста."""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    cleaned_words = [clean_text(w) for w in words]
    unique_words = len(set(cleaned_words))
    word_freq = Counter(cleaned_words)
    top_words = word_freq.most_common(5)
    return {
        'chars_total': len(text),
        'chars_no_spaces': len(text.replace(' ', '').replace('\n', '')),
        'words_count': len(words),
        'sentences_count': len(sentences),
        'unique_words': unique_words,
        'avg_word_length': round(sum(len(w) for w in words) / len(words), 1) if words else 0,
        'top_words': [(w, c) for w, c in top_words if len(w) > 2][:5]
    }


def get_keywords(text: str, top_n: int = 10) -> List[str]:
    """Выделяет ключевые слова текста."""
    cleaned = clean_text(text)
    words = nltk.word_tokenize(cleaned)
    stop_words = {
        'и', 'в', 'на', 'не', 'что', 'с', 'а', 'но', 'за', 'по', 'из', 'у', 'о', 'об',
        'к', 'от', 'до', 'для', 'без', 'через', 'над', 'под', 'про', 'же', 'бы', 'ли',
        'ну', 'вот', 'это', 'тот', 'этот', 'так', 'там', 'тут', 'где', 'когда', 'тогда',
        'потом', 'ещё', 'уже', 'даже', 'ведь', 'вдруг'
    }
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    freq = Counter(keywords)
    return [w for w, c in freq.most_common(top_n)]


def analyze_sentiment(text: str) -> dict:
    """Анализирует тональность текста."""
    return analyze_sentiment_simple(text)


def generate_wordcloud(text: str) -> str:
    """Генерирует облако слов."""
    if not text or len(text.strip()) < 10:
        return ""

    cleaned = clean_text(text)

    stopwords = {
        'и', 'в', 'на', 'не', 'что', 'с', 'а', 'но', 'за', 'по', 'из', 'у', 'о', 'об',
        'к', 'от', 'до', 'для', 'без', 'через', 'над', 'под', 'про', 'же', 'бы', 'ли',
        'ну', 'вот', 'это', 'тот', 'этот', 'так', 'там', 'тут', 'где', 'когда', 'тогда',
        'потом', 'ещё', 'уже', 'даже', 'ведь', 'вдруг', 'как', 'так', 'все', 'было',
        'его', 'её', 'еще', 'или', 'они', 'мы', 'вы', 'ты', 'она', 'он', 'оно'
    }

    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            stopwords=stopwords,
            max_words=100,
            contour_width=1,
            contour_color='steelblue'
        ).generate(cleaned)

        img_buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='PNG', dpi=100, bbox_inches='tight')
        plt.close()

        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        print(f"WordCloud error: {e}")
        return ""


class PlagiarismDetector:
    """Класс для обнаружения заимствований в текстах."""

    def __init__(self) -> None:
        """Инициализирует пустой индекс и список документов."""
        self.index: Dict[str, Set[int]] = defaultdict(set)
        self.documents: List = []

    def add_document(self, doc_id: int, raw_text: str, title: str = "") -> int:
        """Добавляет документ в индекс."""
        cleaned = clean_text(raw_text)
        for ngram in get_ngrams(cleaned):
            self.index[ngram].add(doc_id)
        self.documents.append((doc_id, raw_text, cleaned, title))
        return doc_id

    def find_candidates(self, text: str) -> Set[int]:
        """Находит потенциальные документы-источники."""
        cleaned = clean_text(text)
        candidates = set()
        for ngram in get_ngrams(cleaned):
            candidates.update(self.index.get(ngram, set()))
        return candidates

    def compute_similarity(self, t1: str, t2: str) -> float:
        """Вычисляет сходство между двумя текстами."""
        vec = TfidfVectorizer(tokenizer=nltk.word_tokenize, lowercase=False)
        try:
            m = vec.fit_transform([t1, t2])
            return float(cosine_similarity(m[0:1], m[1:2])[0][0])
        except Exception:
            return 0.0

    def find_common_snippets(self, t1: str, t2: str, min_len: int = 30) -> List[str]:
        """Находит общие фрагменты между текстами."""
        w1, w2 = t1.split(), t2.split()
        snippets = []
        for i in range(len(w1)):
            for j in range(len(w2)):
                length = 0
                while (i + length < len(w1) and
                       j + length < len(w2) and
                       w1[i + length] == w2[j + length]):
                    length += 1
                if length >= 3:
                    snippet = ' '.join(w1[i:i + length])
                    if len(snippet) >= min_len:
                        snippets.append(snippet)
        snippets = list(set(snippets))
        snippets.sort(key=len, reverse=True)
        return snippets[:10]

    def clear(self) -> None:
        """Очищает индекс и список документов."""
        self.index.clear()
        self.documents.clear()


detector = PlagiarismDetector()
