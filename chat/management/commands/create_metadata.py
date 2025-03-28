# chat/management/commands/create_metadata.py
from django.core.management.base import BaseCommand
from chat.utils import create_model_metadata_file

class Command(BaseCommand):
    help = "Generate model metadata JSON file."

    def handle(self, *args, **kwargs):
        create_model_metadata_file()
        self.stdout.write(self.style.SUCCESS("model_metadata.json 파일이 생성되었습니다."))
