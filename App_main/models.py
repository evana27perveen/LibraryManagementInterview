from django.contrib.auth.models import User
from django.db import models

# Create your models here.
categories = {
    ('Fantasy', 'Fantasy'),
    ('Adventure', 'Adventure'),
    ('Romance', 'Romance'),
    ('Contemporary', 'Contemporary'),
    ('Dystopian', 'Dystopian'),
    ('Mystery', 'Mystery'),
    ('Horror', 'Horror'),
    ('Thriller', 'Thriller'),
    ('Paranormal', 'Paranormal'),
    ('Historical fiction', 'Historical fiction'),
    ('Science Fiction', 'Science Fiction'),
    ("Children’s", "Children’s"),
}


class BookModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(choices=categories, max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author}'s Book - {self.title}"


class BorrowBookModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='borrowed_book')
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_by_member')
    borrow_status = models.BooleanField(default=False)




