from urllib import request
from django.db import models
from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min, F, ExpressionWrapper, FloatField
from .models import Book, Student, Address, Publisher

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def one_book(request):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def links(request):
    return render(request, "bookmodule/links.html")

def formatting(request):
    return render(request, "bookmodule/formatting.html")

def listing(request):
    return render(request, "bookmodule/listing.html")

def tables(request):
    return render(request, "bookmodule/tables.html")

def getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        
        if isTitle and isAuthor:
            books = Book.objects.filter(Q(title__icontains=string) | Q(author__icontains=string))
        elif isTitle:
            books = Book.objects.filter(title__icontains=string)
        elif isAuthor:
            books = Book.objects.filter(author__icontains=string)
        else:
            books = Book.objects.all()
            
        return render(request, 'bookmodule/bookList.html', {'books': books})
    
    return render(request, 'bookmodule/search.html')

def simple_query(request):
   mybooks = Book.objects.filter(title__icontains='and') 
   return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(title__icontains='and')\
                         .filter(edition__gte=2)\
                         .exclude(price__lte=100)[:10]
    
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_list.html', {'books': books})

def lab8_task2(request):
    query = Q(edition__gt=3) & (Q(title__icontains='qu'))
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/lab8_list.html', {'books': books})

def lab8_task3(request):
    query = Q(edition__lte=3) & ~Q(title__icontains='qu')
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/lab8_list.html', {'books': books})

def lab8_task4(request):
    books = Book.objects.order_by('title')
    return render(request, 'bookmodule/lab8_list.html', {'books': books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/lab8_stats.html', {'stats': stats})

def lab8_task7(request):
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/lab8_city_stats.html', {'cities': cities})

def lab9_task1(request):
    total_q = Book.objects.aggregate(total=Sum('quantity'))['total'] or 1
    books = Book.objects.annotate(
        availability_pct=ExpressionWrapper(
            (F('quantity') * 100.0) / total_q, output_field=FloatField()
        )
    )
    return render(request, 'bookmodule/lab9_task1.html', {'books': books})

def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/lab9_list.html', {'publishers': publishers, 'task_num': 2})

def lab9_task3(request):
    publishers = Publisher.objects.annotate(oldest_book=Min('book__pubdate'))
    return render(request, 'bookmodule/lab9_list.html', {'publishers': publishers, 'task_num': 3})

def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_p=Avg('book__price'), 
        min_p=Min('book__price'), 
        max_p=Max('book__price')
    )
    return render(request, 'bookmodule/lab9_list.html', {'publishers': publishers, 'task_num': 4})

def lab9_task5(request):
    publishers = Publisher.objects.filter(book__rating__gte=4).annotate(
        book_count=Count('book')
    )
    return render(request, 'bookmodule/lab9_list.html', {'publishers': publishers, 'task_num': 5})

def lab9_task6(request):
    publishers = Publisher.objects.filter(
        book__price__gt=50,
        book__quantity__lt=5,
        book__quantity__gte=1
    ).annotate(book_count=Count('book'))
    return render(request, 'bookmodule/lab9_list.html', {'publishers': publishers, 'task_num': 6})