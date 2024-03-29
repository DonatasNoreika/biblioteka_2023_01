
from django.urls import path, include
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.index, name="index"),
    path('authors/', views.authors, name="authors"),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name="books"),
    path('books/<int:pk>', views.BookDetailView.as_view(), name="book"),
    path('search/', views.search, name="search"),
    path("register/", views.register, name="register"),
    path("profilis/", views.profilis, name="profilis"),
    path("userbooks/", views.UserBookInstanceListView.as_view(), name="user_books"),
    path("userbooks/<int:pk>", views.UserBookInstanceDetailView.as_view(), name="user_book"),
    path('userbooks/create', views.UserBookInstanceCreateView.as_view(), name='user_bookinstance_create'),
    path("userbooks/<int:pk>/update", views.UserBookInstanceUpdateView.as_view(), name="user_bookinstance_update"),
    path('userbooks/<int:pk>/delete', views.UserBookInstanceDeleteView.as_view(), name="user_bookinstance_delete"),
    path("bookinstances/<int:inst_id>/paimti", views.paimti, name="paimti"),
    path("bookinstances/<int:inst_id>/grazinti", views.grazinti, name="grazinti"),
]