from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    return render(request, 'index.html', context=context)

def authors(request):
    paginator = Paginator(Author.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        'author': author,
    }
    return render(request, 'author.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 4
    template_name = 'books.html'
    context_object_name = "books"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = "book"

def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', context={'books': search_results, 'query': query})


class UserBookInstanceListView(generic.ListView, LoginRequiredMixin):
    model = BookInstance
    paginate_by = 4
    template_name = 'user_books.html'
    context_object_name = "instances"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')