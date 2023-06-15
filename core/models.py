from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField("name", max_length=255, primary_key=True, db_index=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    isbn = models.PositiveBigIntegerField(db_index=True, primary_key=True)
    name = models.CharField(max_length=1000, db_index=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(Author, related_name="book_author", on_delete=models.DO_NOTHING, null=True, blank=True)
    reserve = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    STATUS = (
        ('DEFAULT', 'default'),
        ('IN_USE', 'In_use'),
        ('DONE', 'Done'),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    book_in_order = models.ManyToManyField(Book)
    to_change = models.BooleanField(default=False)
    mod_after_created = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=10)
    start = models.DateField(db_index=True, null=False, blank=False)
    end = models.DateField(db_index=True, null=False, blank=False)
