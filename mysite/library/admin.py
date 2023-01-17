from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0  # išjungia papildomas tuščias eilutes įvedimui

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')

    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back')}),
    )

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)