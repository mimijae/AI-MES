# chat/utils.py
import logging
from django.apps import apps
from django.conf import settings
import json
import os

def get_django_model_metadata():
    """Django 모델 메타데이터를 추출하여 딕셔너리 형태로 반환"""
    model_metadata = {}
    for model in apps.get_models():
        fields = {field.name: field.get_internal_type() for field in model._meta.get_fields()}
        model_metadata[model.__name__] = fields
    return model_metadata

# JSON 파일 생성 (생성된 파일은 chat 디렉토리에 저장)
def create_model_metadata_file():
    """model_metadata.json 파일을 생성"""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # chat 폴더 경로
    metadata_path = os.path.join(base_dir, 'model_metadata.json')
    with open(metadata_path, 'w', encoding="utf-8") as f:
        json.dump(get_django_model_metadata(), f, ensure_ascii=False, indent=4)
