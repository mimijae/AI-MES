# chat/apps.py
from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        """앱이 로드될 때 model_metadata.json 파일을 생성"""
        from .utils import create_model_metadata_file
        create_model_metadata_file()
