from django.core.management.base import BaseCommand
from optparse import make_option
from sam.models import Website
import os


class Command(BaseCommand):
    help = 'This creates Website objects from text file input or writes Websites to text file'

    option_list = BaseCommand.option_list + (
        make_option('-r',
                    '--read',
                    dest='read',
                    default=False,
                    action='store_true',
                    help='This will create Website objects from a text file.'),
        make_option('-w',
                    '--write',
                    dest='write',
                    default=False,
                    action='store_true',
                    help='This will create a text file with Website objects.'),
    )

    def handle(self, *args, **options):
        write = options['write']
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'websites.txt')
        if not write:
            site_file = open(file_path, 'r')
            for line in site_file:
                if len(line.strip()) > 0:
                    parts = line.split("-=-")
                    url = parts[0].strip()
                    display = parts[1].strip()
                    kind = parts[2].strip()
                    Website(url=url, display=display, kind=kind).save()
        else:
            site_file = open(file_path, 'w')
            for site in Website.objects.all():
                line = site.url + '-=-' + site.display + '-=-' + site.kind
                quote_file.write(line + "\n")
