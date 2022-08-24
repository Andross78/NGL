from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(NumericFilterModelAdmin):


    list_display = ('name', 'api_key', 'views')
    list_display_links = ('name',)

    list_filter = (('views', RangeNumericFilter),)


admin.site.register(Book)