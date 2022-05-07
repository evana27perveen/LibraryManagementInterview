"# LibraryManagementInterview"  "# LibraryManagementInterview" 

**Authentication Actions**
**Signup URL:** http://domain_name/accouts/registerAPI/

Necessary fields to signup: username, email, password, password2, groups(groups 1/2: 1 is Member, 2 is Librarian)

**Login URL:** http://domain_name/accouts/token/, http://domain_name/accouts/token/refresh/ (Refresh token is to get new access token)

Necessary fields to Login: username, password

**Librarian Actions**

Librarian Dashboard: http://domain_name/librarian-dashboard/ 

Librarian can add new book: http://domain_name/add-new-book/

Librarian can Update book: http://domain_name/update-book/<int:id>/

Librarian can remove book: http://domain_name/remove-book/<int:id>/

Librarian can see all user: http://domain_name/all-users/

Librarian can add new user: http://domain_name/add-user/

Librarian can update user: http://domain_name/update-user/<int:id>/

Librarian can delete user: http://domain_name/delete-user<int:id>/


**Member's Actions**

Member can see all books: http://domain_name/member-library-view/

Member can borrow books: http://domain_name/member-book-borrow-view/<int:id>/

Member can return borrowed books: http://domain_name/member-return-view/<int:id>/

Member can delete his/her account: http://domain_name/member-own-delete-view/


