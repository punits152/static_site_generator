# Create your views here.
import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join

def get_page_or_404(name):
    print("getting")
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY,name) #Here added an absolute path to our pages that wil be given by the url
    except ValueError:
        raise Http404(f"{file_path} Not Found")
    else:
        if not os.path.exists(file_path):
            raise Http404(f"{file_path} Not Found")
    
    with open(file_path,'r') as f:
        page = Template(f.read())
    
    return page

def page(request,slug='index'):
    "Render the request html page"
    filename = '{}.html'.format(slug)
    page = get_page_or_404(filename)
    context = {
        "slug":slug,
        "page":page
    }
    
    return render(request,"page.html",context)
