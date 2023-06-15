from django.contrib import admin
from .models import (
    Book,
    Author, Order
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_display_links = (
        'name',
    )
    list_filter = (
        'name',
    )
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'isbn', 'quantity'
    )
    list_display_links = (
        'name', 'isbn',
    )
    list_editable = (
        'quantity',
    )
    search_fields = ('name', 'isbn', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
