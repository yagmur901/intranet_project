from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import TrigramWordSimilarity 
from django.db.models.functions import Greatest
from django.core.paginator import Paginator
from .models import Employee

def employee_list_view(request):
    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '').strip()
    
    employees = Employee.objects.all()

    departments = (
        Employee.objects.exclude(department__isnull=True)
        .exclude(department__exact='')
        .values_list('department', flat=True)
        .distinct()
        .order_by('department')
    )

    if query:
        clean_query = query.replace('I', 'ı').replace('İ', 'i').lower()
        
        employees = employees.annotate(
            max_similarity=Greatest(
                TrigramWordSimilarity(query, 'first_name'),
                TrigramWordSimilarity(query, 'last_name'),
                TrigramWordSimilarity(query, 'short_name'),
                TrigramWordSimilarity(query, 'department'),
                TrigramWordSimilarity(query, 'email')
            )
        ).filter(
            Q(first_name__unaccent__icontains=clean_query) |
            Q(last_name__unaccent__icontains=clean_query) |
            Q(short_name__unaccent__icontains=clean_query) |
            Q(department__unaccent__icontains=clean_query) |
            Q(email__unaccent__icontains=clean_query) |
            Q(phone_number__unaccent__icontains=clean_query) |
            Q(max_similarity__gt=0.3)
        ).order_by('-max_similarity', 'first_name', 'last_name')

    if department:
        employees = employees.filter(department__iexact=department)
        
    if not query:
        employees = employees.order_by('first_name', 'last_name')
        
    paginator = Paginator(employees, 20)  # her sayfada 20 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_dep': department, 
        'departments': departments
    }

    return render(request, 'employee_list.html', context)