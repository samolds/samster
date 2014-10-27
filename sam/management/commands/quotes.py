from django.core.management.base import BaseCommand
from optparse import make_option
from sam.models import Quote
import os


class Command(BaseCommand):
    help = 'This creates Quote objects from text file input or writes Quotes to text file'

    option_list = BaseCommand.option_list + (
        make_option('-r',
                    '--read',
                    dest='read',
                    default=False,
                    action='store_true',
                    help='This will create Quote objects from a text file.'),
        make_option('-w',
                    '--write',
                    dest='write',
                    default=False,
                    action='store_true',
                    help='This will create a text file with Quote objects.'),
    )

    def handle(self, *args, **options):
        write = options['write']
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'quotes.txt')
        if not write:
            quote_file = open(file_path, 'r')
            for line in quote_file:
                if len(line.strip()) > 0:
                    parts = line.split("-=-")
                    quote = parts[0].strip()
                    author = parts[1].strip()
                    Quote(quote=quote, author=author).save()
        else:
            quote_file = open(file_path, 'w')
            for quote in Quote.objects.all():
                quote_file.write(quote.quote + " -=- " + quote.author + "\n")
