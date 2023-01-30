from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, BookReview, Profilis

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    readonly_fields = ['uuid']
    can_delete = False
    extra = 0  # išjungia papildomas tuščias eilutes įvedimui

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')

    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'reader')
    list_filter = ('status', 'due_back')
    search_fields = ("uuid", "book__title")
    list_editable = ('due_back', 'status', 'reader')

    # fieldsets = (
    #     ('General', {'fields': ('uuid', 'book')}),
    #     ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    # )

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'date_created', 'reviewer', 'content')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Profilis)