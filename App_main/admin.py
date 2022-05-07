from django.contrib import admin
from App_main.models import BookModel, BorrowBookModel

# Register your models here.
admin.site.register(BookModel)
admin.site.register(BorrowBookModel)
