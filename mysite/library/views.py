from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookInstanceCreateForm
from django.contrib.auth.decorators import login_required


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


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = "book"
    form_class = BookReviewForm
    
    def get_success_url(self):
        return reverse("book", kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', context={'books': search_results, 'query': query})


class UserBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 4
    template_name = 'user_books.html'
    context_object_name = "instances"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


class UserBookInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = "user_book.html"
    context_object_name = "instance"


class UserBookInstanceCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    # fields = ['book', 'due_back', 'status']
    success_url = "/library/userbooks/"
    template_name = "user_bookinstance_form.html"
    form_class = UserBookInstanceCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.save()
        return super().form_valid(form)

class UserBookInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    # fields = ['book', 'due_back', 'status']
    success_url = "/library/userbooks/"
    template_name = "user_bookinstance_form.html"
    form_class = UserBookInstanceCreateForm

    def test_func(self):
        bookinstance = self.get_object()
        return bookinstance.reader == self.request.user

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.save()
        return super().form_valid(form)


class UserBookInstanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    success_url = "/library/userbooks/"
    template_name = "user_bookinstance_delete.html"
    context_object_name = "instance"

    def test_func(self):
        bookinstance = self.get_object()
        return bookinstance.reader == self.request.user

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


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context=context)