from django.shortcuts import render, get_object_or_404
from .models import CorpusDocument

def corpus_list(request):
    docs = CorpusDocument.objects.all()
    return render(request, 'core/corpus_list.html', {'docs': docs})

def document_detail(request, doc_id):
    doc = get_object_or_404(CorpusDocument, id=doc_id)
    return render(request, 'core/document_detail.html', {'doc': doc})
