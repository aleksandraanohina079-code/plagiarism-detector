import re
from collections import Counter

# Простой словарь позитивных и негативных слов для русского языка
positive_words = {
    'хороший', 'отличный', 'прекрасный', 'замечательный', 'великий',
    'любить', 'люблю', 'нравится', 'радость', 'счастье', 'успех',
    'добрый', 'светлый', 'тёплый', 'красивый', 'чудесный', 'восторг',
    'позитивный', 'великолепный', 'блестящий', 'удивительный',
    'молодец', 'умница', 'прекрасно', 'отлично', 'здорово'
}

negative_words = {
    'плохой', 'ужасный', 'отвратительный', 'страшный', 'злой',
    'ненавидеть', 'ненавижу', 'грусть', 'печаль', 'боль', 'страдание',
    'проблема', 'трудность', 'сложность', 'кризис', 'катастрофа',
    'гнев', 'злость', 'разочарование', 'уныние', 'тоска', 'обида',
    'страх', 'ужас', 'кошмар', 'позор', 'унижение'
}

def analyze_sentiment_simple(text: str) -> dict:
    """
    Простой анализ тональности на основе словарей позитивных/негативных слов
    """
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_count = sum(1 for w in words if w in positive_words)
    negative_count = sum(1 for w in words if w in negative_words)
    
    total = positive_count + negative_count
    if total == 0:
        return {
            'label': 'нейтральная',
            'color': '#6c757d',
            'emoji': '😐',
            'score': 0.5,
            'message': 'Текст имеет нейтральную окраску'
        }
    
    sentiment_score = (positive_count - negative_count) / total
    
    if sentiment_score > 0.2:
        return {
            'label': 'позитивная',
            'color': '#28a745',
            'emoji': '😊',
            'score': sentiment_score,
            'message': f'Текст имеет позитивную окраску (+{positive_count} / -{negative_count})'
        }
    elif sentiment_score < -0.2:
        return {
            'label': 'негативная',
            'color': '#dc3545',
            'emoji': '😞',
            'score': abs(sentiment_score),
            'message': f'Текст имеет негативную окраску (+{positive_count} / -{negative_count})'
        }
    else:
        return {
            'label': 'нейтральная',
            'color': '#ffc107',
            'emoji': '😐',
            'score': 0.5,
            'message': 'Текст имеет нейтральную окраску'
        }
