from django.core.management.base import BaseCommand
from sam.models import Tag


class Command(BaseCommand):
    help = 'This creates all hardcoded tag objects'

    def handle(self, *args, **options):
        tags = [
          {'tag': 'top_about', 'description': 'Tag to put post on about page.'},
          {'tag': 'top_contact', 'description': 'Tag to put post on contact page.'},
          {'tag': 'top_education', 'description': 'Tag to put post on education page.'},
          {'tag': 'top_home', 'description': 'Tag to put post on home page.'},
          {'tag': 'top_personal', 'description': 'Tag to put post on personal page.'},
          {'tag': 'top_professional', 'description': 'Tag to put post on professional page.'},
          {'tag': 'personal', 'description': ''},
          {'tag': 'thoughts', 'description': ''},
          {'tag': 'shower_thoughts', 'description': ''},
          {'tag': 'education', 'description': ''},
          {'tag': 'school', 'description': ''},
          {'tag': 'homework', 'description': ''},
          {'tag': 'professional', 'description': ''},
          {'tag': 'work', 'description': ''},
          {'tag': 'job', 'description': ''},
          {'tag': 'experience', 'description': ''},
          {'tag': 'project', 'description': ''},
          {'tag': 'banner_photo', 'description': 'Tag to make an image the home page banner'},
          {'tag': 'art', 'description': ''},
          {'tag': 'drawing', 'description': ''},
          {'tag': 'photography', 'description': ''},
          ]
        for tag in tags:
            Tag(tag=tag['tag'], description=tag['description']).save()
