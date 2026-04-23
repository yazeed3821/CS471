from django.contrib import admin
from .models import Book, Student, Address

admin.site.register(Book)
admin.site.register(Address)
admin.site.register(Student)