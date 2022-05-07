from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
# Rest Framework view Import
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
# From App_auth Imports
from rest_framework.response import Response
from rest_framework.views import APIView

from App_auth.serializers import UserModelSerializer, RegisterSerializer, UserUpdatingSerializer
# From App_main Imports
from App_main.models import BookModel, BorrowBookModel
from App_main.serializers import BookModelSerializer, BorrowBookModelSerializer


# Create your views here.
class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='LIBRARIAN'):
            return True
        return False


class DashboardAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian, ]
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer


class AddNewBookAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer


class UpdateBookAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    lookup_field = 'id'


class RemoveBookAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    lookup_field = 'id'


# User controlled by the Librarian
class AllUserAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class AddUserAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UpdateUserAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = User.objects.all()
    serializer_class = UserUpdatingSerializer
    lookup_field = 'id'


class RemoveUserAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'


# Library Member's section
class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='MEMBER'):
            return True
        return False


class MemberLibraryView(ListAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = BookModel.objects.filter(available=True)
        return queryset


class MemberBorrowBook(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request, bookID, *args, **kwargs):
        user = request.user
        book = BookModel.objects.get(id=bookID)
        borrowBookObject = BorrowBookModel.objects.filter(book=book, borrowed_by=user)
        if borrowBookObject.exists() and borrowBookObject[0].borrow_status:
            return Response({"Error": "Already borrowed a book, you have to return that first"})
        borrow_book = BorrowBookModel.objects.get_or_create(book=book, borrowed_by=user)
        borrow_book[0].borrow_status = True
        borrow_book[0].save()
        book.quantity -= 1
        book.save()

        return Response({"Status": f"{book.title} has been borrowed by {request.user}"}, status=status.HTTP_200_OK)


class MemberReturnBorrowedBook(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request, bookID, *args, **kwargs):
        user = request.user
        book = BookModel.objects.get(id=bookID)
        borrowBookObject = BorrowBookModel.objects.get(book=book, borrowed_by=user)
        if borrowBookObject.borrow_status:
            borrowBookObject.borrow_status = False
            borrowBookObject.save()
            book.quantity += 1
            book.save()

            return Response({"Status": f"{book.title} has been returned by {request.user}"}, status=status.HTTP_200_OK)

        return Response({"Error": "You didn't borrow the book, or you have already returned the book!"})


def no_return_pending(borrowList, userBorrowStatus):
    if len(borrowList) == 0:
        return userBorrowStatus
    else:
        if borrowList[0].borrow_status:
            return "Pending"
        else:
            userBorrowStatus = 'No Pending'
            borrowList.remove(borrowList[0])
        return no_return_pending(borrowList, userBorrowStatus)


class DeleteMemberAccount(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def delete(self, request, *args, **kwargs):
        allBorrowed = BorrowBookModel.objects.filter(borrowed_by=request.user)
        anyMoreBorrow = no_return_pending(list(allBorrowed), "No Pending")
        if anyMoreBorrow == "Pending":
            return Response(
                {"Error": "You didn't return the book that you borrowed, so your account can't be deleted!"})
        User.objects.get(id=request.user.id).delete()
        return Response({"Success": "Your ID has been deleted!"})
