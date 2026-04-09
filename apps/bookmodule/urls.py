from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='books.index'),
    path('list_books/', views.list_books, name='books.list_books'),
    path('one_book/', views.one_book, name='books.one_book'),
    path('aboutus/', views.aboutus, name='books.aboutus'),
    path('html5/links/', views.links),
    path('html5/text/formatting/', views.formatting),
    path('html5/listing/', views.listing),
    path('html5/tables/', views.tables),
    path('search/', views.search, name="books.search"),
]