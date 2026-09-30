from django.shortcuts import render
from django.db.models import Q
from .models import DocumentCategory, Document

def document_list_view(request):
    query = request.GET.get('q', '')
    selected_cat_id = request.GET.get('category', '')
    selected_doc_id = request.GET.get('doc_id', '')  # arama motorundan tıklanan doküman ID

    categories = DocumentCategory.objects.all()
    documents = Document.objects.select_related('category').all()

    # eğer arama sonuçlarından doğrudan bir dokümana tıklanarak gelindiyse sadece onu göster
    if selected_doc_id:
        documents = documents.filter(id=selected_doc_id)

    # kategori seçildiyse filtrele
    if selected_cat_id:
        documents = documents.filter(category_id=selected_cat_id)

    # kelime araması yapıldıysa filtrele
    if query:
        clean_query = query.replace('I', 'ı').replace('İ', 'i').lower()
        documents = documents.filter(
            Q(title__unaccent__icontains=clean_query) |
            Q(description__unaccent__icontains=clean_query)
        )

    context = {
        'documents': documents,
        'categories': categories,
        'query': query,
        'selected_cat_id': selected_cat_id,
        'selected_doc_id': selected_doc_id,  # şablonda "Tüm Dokümanlara Dön" butonu çıkarmak için
    }
    return render(request, 'document_list.html', context)