from ast import Interactive
from lib2to3.pytree import Base
import os
import shutil
from urllib import response

from django.conf import settings
from django.core.management import BaseCommand,call_command, CommandError
from django.urls import reverse
from django.test.client import Client

def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith(".html"):
            yield name[:-5]


class Command(BaseCommand):
    help = "Basic static site output"

    def handle(self,*args,**options):

        settings.DEBUG = False
        settings.COMPRESS_ENABLED = True

        if args:
            pages = args
            available = list(get_pages())
            invalid = []
            for page in pages:
                if page not in available:
                    invalid.append(page)

            if invalid:
                msg = "Invalid Pages: {}".format(', '.join(invalid))
                raise CommandError(msg)

        else:

            # If the directory is there just remove it
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
            os.makedirs(settings.STATIC_ROOT)

            call_command('collectstatic',  clear=True, verbosity=0)
            call_command('compress',  force=True)

            client = Client()

            pages = get_pages()

            for page in pages:
                url = reverse('page',kwargs={"slug":page})

                response = client.get(url)

                if page == 'index':
                    output_dir = settings.SITE_OUTPUT_DIRECTORY
                else:
                    output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY,page)
                    os.makedirs(output_dir)

                with open(os.path.join(output_dir,f"{page}.html"),'wb') as f:
                    print(page)
                    f.write(response.content)




