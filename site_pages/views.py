# Create your views here.
import enum
import json
import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template, Context
from django.utils._os import safe_join
from django.template.loader_tags import BlockNode

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

    #Here getting all the blocks that have block tag name context 
    #We will provide a daata in there for the components to use in the html and will provide them as contet to the same html code
    meta = None
    for i, node in enumerate(list(page.nodelist)):
        if isinstance(node,BlockNode) and node.name=='context':
            meta = page.nodelist.pop(i)
            break
    
    page._meta = meta
    return page

def page(request,slug='index'):
    "Render the request html page"
    filename = '{}.html'.format(slug)
    page = get_page_or_404(filename)
    context = {
        "slug":slug,
        "page":page
    }
    
    if page._meta is not None:
        meta = page._meta.render(Context())
        extra_context = json.loads(meta)

        # Provide the context block data back  to the same dictionary
        # this will be used in the html pages
        context.update(extra_context)

    return render(request,"page.html",context)
