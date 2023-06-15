from datetime import datetime
from celery_singleton import Singleton
from django.db import transaction
from core.models import Author, Book, Order
from settings.celery import app


@app.task(base=Singleton)
def orders_with_dept():
    to_return = Order.objects.filter(status__in=('IN_USE', 'In_use'), end__lte=datetime.utcnow())


@app.task(base=Singleton)
def upload_books(*args, **kwargs) -> None:
    data = kwargs['payload']
    authors = {}
    books = []
    for book in data:
        if not authors.get(book['author'], None):
            authors[book['author']] = Author(name=book['author'])
        books.append(
            Book(
                name=book['name'],
                isbn=book['isbn'],
                quantity=book['quantity'],
                author_id=book['author']
            )
        )
    Author.objects.bulk_create(list(authors.values()), ignore_conflicts=True)
    Book.objects.bulk_create(books, ignore_conflicts=True)


@app.task(base=Singleton, bind=True, max_retries=10)
def upload_m2m_model(self, *args, **kwargs) -> None:
    try:
        obj_pk = kwargs['payload']
        with transaction.atomic():
            obj = Order.objects.prefetch_related('book_in_order').select_for_update().get(pk=int(obj_pk))
            if not obj.mod_after_created:
                if obj.reserved:
                    books = obj.book_in_order.all()
                    updated_books = []
                    for book in books:
                        if book.quantity > 0:
                            book.reserve += 1
                            book.quantity -= 1
                            updated_books.append(book)
                        else:
                            obj.book_in_order.remove(book)
                    Book.objects.bulk_update(updated_books, ['reserve', 'quantity'])
                obj.mod_after_created = True

            if (obj.status in ('IN_USE', 'In_use')) and obj.reserved:
                books = obj.book_in_order.all()
                updated_books = []
                for book in books:
                    book.reserve -= 1
                    updated_books.append(book)
                Book.objects.bulk_update(updated_books, ['reserve'])

            elif (obj.status in ('IN_USE', 'In_use')) and (not obj.reserved):
                books = obj.book_in_order.all()
                updated_books = []
                for book in books:
                    if book.quantity > 0:
                        book.quantity -= 1
                        updated_books.append(book)
                    else:
                        obj.book_in_order.remove(book)
                Book.objects.bulk_update(updated_books, ['quantity'])

            elif obj.status in ('DONE', 'Done'):
                books = obj.book_in_order.all()
                updated_books = []
                for book in books:
                    book.quantity += 1
                    updated_books.append(book)
                Book.objects.bulk_update(updated_books, ['quantity'])
            obj.to_change = False
            obj.save()

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
