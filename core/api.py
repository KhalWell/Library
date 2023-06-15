from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from core.utils.file_parsers.csv_parser import BaseParser
from .models import Author, Book, Order
from .serializers import BaseBookSerializer, CUBookSerializer, BaseAuthorSerializer, \
    CUUserSerializer, RDUserSerializer, BaseOrderSerializer, BookWithReturnTimeSerializer
from .service.permissions import IsAdminOrLibraryMan, IsAdminOrLibraryManOrReadOnly
from .tasks import upload_books


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderApiSet(viewsets.ModelViewSet):
    """
        CRUD по книгам
    """
    pagination_class = CommonPagination
    queryset = Order.objects.prefetch_related('book_in_order').all()
    serializer_class = BaseOrderSerializer
    permission_classes = (IsAdminOrLibraryMan,)


class BookApiSet(viewsets.ModelViewSet):
    """
        CRUD по книгам
    """
    pagination_class = CommonPagination
    queryset = Book.objects.select_related('author').all()
    serializer_class = CUBookSerializer
    permission_classes = (IsAdminOrLibraryManOrReadOnly,)

    def get_object(self):
        obj = super().get_object()
        if self.request.method == 'GET' and self.kwargs.get('pk'):
            try:
                returned = Order.objects.prefetch_related('book_in_order').filter(
                    book_in_order__isbn=obj.isbn).order_by('end')[0].end
                obj.returned = returned
            except IndexError:
                obj.returned = ''
            self.serializer_class = BookWithReturnTimeSerializer
        elif self.request.method not in ['PATCH', 'PUT', 'POST']:
            self.serializer_class = BaseBookSerializer

        return obj

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method not in ['PATCH', 'PUT', 'POST']:
            self.serializer_class = BaseBookSerializer
        return qs


class AuthorApiSet(viewsets.ModelViewSet):
    """
        CRUD по авторам
    """
    pagination_class = CommonPagination
    queryset = Author.objects.all()
    serializer_class = BaseAuthorSerializer
    permission_classes = (IsAdminOrLibraryMan,)


class UserApiSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    pagination_class = CommonPagination
    queryset = User.objects.prefetch_related('groups').filter(is_staff=False, is_superuser=False).exclude(
        groups__name='LibraryMan')
    serializer_class = CUUserSerializer
    permission_classes = (IsAdminOrLibraryMan,)

    def get_object(self):
        if self.request.method not in ['PATCH', 'PUT', 'POST']:
            self.serializer_class = RDUserSerializer
        return super().get_object()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method not in ['PATCH', 'PUT', 'POST']:
            self.serializer_class = RDUserSerializer
        if not self.kwargs.get('pk'):
            self.serializer_class = RDUserSerializer
        return qs


class BookUploadCSVView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [permissions.AllowAny]

    def post(self, request, filename, format=None):
        payload = request.data.get('file', None)
        if payload:
            data = BaseParser.to_json(BaseParser.pars_file(payload, header=0, delimiter=';'), orient='records')
            upload_books.delay(payload=data)
            payload.close()
            return Response({'status': 200, 'message': 'File uploaded.'})
        return Response({'status': 200, 'message': 'No File.'})
