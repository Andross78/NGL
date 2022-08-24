from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, ListAPIView)
import django_filters.rest_framework
from django.core.paginator import Paginator

import mimetypes
import os
import requests
import csv

from .models import Author, Book
from .forms import AuthorForm
from .serializers import AuthorSerializer

@transaction.atomic
def index(request):
    
    form = AuthorForm(request.POST)
    authors = Author.objects.all()

    p = Paginator(authors, 10)
    page = request.GET.get('page')
    author_per_page = p.get_page(page)

    message = None
    ctx = {
        'form': form,
        'authors': authors,
        'message': message,
        'author_per_page': author_per_page,
    }
    if request.method == 'POST':
        
        if form.is_valid():
            author_name_from_post = request.POST['author_name']
            author_name = '%20'.join(author_name_from_post.split())
            api_url = 'https://openlibrary.org/search/authors.json?q='
            r = requests.get(api_url + author_name)
            response = r.json()

            if len(response['docs']) != 0:
                try:
                    for person in response['docs']:
                        author = Author.objects.get(api_key=person['key'])
                        author.views += 1
                        author.save()

                except Author.DoesNotExist:
                    data = response['docs']
                    for person in data:
                        new_author = Author()
                        if 'name' in person:
                            new_author.name = person['name']
                        if 'key' in person:
                            new_author.api_key = person['key']
                        if 'alternate_names' in person:
                            new_author.aka = person['alternate_names']
                        new_author.views = 1
                        new_author.save(Author())
                        
            else:
                if ('_' in author_name_from_post):
                    ctx['message'] = 'Wrong character in author name field: _'

            render(request, 'index.html', ctx)
    
    return render(request, 'index.html', ctx)


def import_csv(request):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'authors.csv'
    filepath = BASE_DIR + '/' + filename
    authors = Author.objects.all()
    with open(filename, 'w') as f:

        
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        fieldnames = ['Name', 'API Key', 'Views']
        writer.writerow(fieldnames)
        for author in authors:
            writer.writerow([author.name, author.api_key, author.views])

    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class AuthorListView(ListAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'views']

    # def get_queryset(self):
    #     filter_name = self.kwargs['filter_name']
    #     return Author.objects.filter(name__contains=filter_name)


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer