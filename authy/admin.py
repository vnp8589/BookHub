from django.contrib import admin
from authy.models import Profile, books, BookReview
# Register your models here.

admin.site.register(Profile)
admin.site.register(books)
admin.site.register(BookReview)