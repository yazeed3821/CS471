from urllib import request
from django.db import models
from django.shortcuts import render
from django.db.models import Q
from .models import Book

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
    mybooks = Book.objects.filter(author__isnull=False)\
                         .filter(title__icontains='and')\
                         .filter(edition__gte=2)\
                         .exclude(price__lte=100)[:10]
    
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')