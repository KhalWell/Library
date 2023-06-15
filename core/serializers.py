from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Book, Order


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CUUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class RDUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login')


class BaseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BaseBookSerializer(serializers.ModelSerializer):
    author = BaseAuthorSerializer(many=False)

    class Meta:
        model = Book
        fields = "__all__"


class BookWithReturnTimeSerializer(BaseBookSerializer):
    returned = serializers.CharField(required=False, max_length=50, allow_null=True)


class CUBookSerializer(BaseBookSerializer):
    author = serializers.CharField(required=False, max_length=255, allow_null=True)

    def update(self, instance, validated_data):
        author = validated_data.pop("author")
        author_obj, _ = Author.objects.get_or_create(name=author)
        instance.author = author_obj
        instance.save()
        return instance

    def create(self, validated_data):
        author = validated_data.pop("author")
        author_obj, _ = Author.objects.get_or_create(name=author)
        instance = super().create(validated_data)
        instance.author = author_obj
        instance.save()
        return instance


class BaseOrderSerializer(serializers.ModelSerializer):
    book_in_order = BaseBookSerializer(many=True)

    class Meta:
        model = Order
        fields = ('pk', 'user', 'reserved', 'book_in_order', 'status', 'start', 'end')
