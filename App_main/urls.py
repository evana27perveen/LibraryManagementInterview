from django.urls import path
from App_main.views import *

app_name = 'App_main'

urlpatterns = [
    path('dashboard/', DashboardAPIView.as_view()),
    path('add-new-book/', AddNewBookAPIView.as_view()),
    path('update-book/<int:id>/', UpdateBookAPIView.as_view()),
    path('remove-book/<int:id>/', RemoveBookAPIView.as_view()),
    #     All User
    path('all-users/', AllUserAPIView.as_view()),
    path('add-user/', AddUserAPIView.as_view()),
    path('update-user/<int:id>/', UpdateUserAPIView.as_view()),
    path('delete-user/<int:id>/', RemoveUserAPIView.as_view()),
    #     Member's Operations
    path('member-library-view/', MemberLibraryView.as_view()),
    path('member-book-borrow-view/<int:bookID>/', MemberBorrowBook.as_view()),
    path('member-book-return-view/<int:bookID>/', MemberReturnBorrowedBook.as_view()),
    path('member-own-delete-view/', DeleteMemberAccount.as_view()),
]
