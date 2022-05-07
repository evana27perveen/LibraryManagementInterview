from rest_framework import serializers
from App_main.models import BookModel, BorrowBookModel


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = "__all__"


class BorrowBookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowBookModel
        fields = ['borrow_status']


