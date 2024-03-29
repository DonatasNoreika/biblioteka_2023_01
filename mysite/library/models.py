from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200, help_text='Įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = 'Žanrai'


class Book(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    summary = models.TextField(verbose_name=_("Summary"), max_length=1000)
    isbn = models.CharField(verbose_name=_("ISBN"), max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey(to="Author", verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, related_name='books')
    genre = models.ManyToManyField(to="Genre", verbose_name=_("Genre"))
    cover = models.ImageField(verbose_name=_("Cover"), upload_to="covers", null=True, blank=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = _("Genre")

    def __str__(self):
        return f"{self.title} ({self.author})"

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _('Books')


class Author(models.Model):
    first_name = models.CharField(verbose_name='Vardas', max_length=100)
    last_name = models.CharField(verbose_name='Pavardė', max_length=100)
    # description = models.TextField(verbose_name="Aprašymas", max_length=3000, blank=True, default="")
    description = HTMLField(verbose_name="Aprašymas", blank=True, null=True)

    def display_books(self):
        return ", ".join(book.title for book in self.books.all()[:3])

    display_books.short_description = 'Knygos'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = 'Autoriai'


class BookInstance(models.Model):
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, related_name='instances')
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)
    reader = models.ForeignKey(to=User, verbose_name="Skaitytojas", on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.due_back and self.due_back < date.today()

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )

    def __str__(self):
        return f"{self.book} - {self.uuid}"

    class Meta:
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural = 'Knygų egzemplioriai'


class BookReview(models.Model):
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Laikas", auto_now_add=True)
    content = models.TextField(verbose_name="Atsiliepimas", max_length=3000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']


class Profilis(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

