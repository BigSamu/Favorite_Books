from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('books',views.userDetails),
    path('add_book_to_list',views.addBooktoList),
    path('add_book_to_favorites/<int:book_id>',views.addBookToFavorites),
    path('add_book_to_favorites_function_2/<int:book_id>',views.addBookToFavoritesFunctionTwo),
    path('remove_book_from_favorites/<int:book_id>',views.removeBookFromFavorites),
    path('books/<int:book_id>',views.booksDetails),
]

