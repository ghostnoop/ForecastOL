from uuid import uuid4

# util
from django.core.management import BaseCommand

from parser.consumer.consumer import Consumer


class Command(BaseCommand):
    help = "Runs consumer."

    def handle(self, *args, **options):
        print("started ")

        worker()


def worker():
    Consumer().start_consume()
