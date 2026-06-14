from django.shortcuts import render, get_object_or_404
from .models import CorpusDocument


def corpus_list(request):
    """
    Отображает список всех документов в корпусе.

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: Страница со списком документов
    """
    docs = CorpusDocument.objects.all()
    return render(request, 'core/corpus_list.html', {'docs': docs})


def document_detail(request, doc_id):
    """
    Отображает полный текст документа по его ID.

    Args:
        request: HTTP-запрос
        doc_id (int): ID документа

    Returns:
        HttpResponse: Страница с текстом документа
    """
    doc = get_object_or_404(CorpusDocument, id=doc_id)
    return render(request, 'core/document_detail.html', {'doc': doc})
