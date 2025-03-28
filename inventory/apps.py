from django.apps import AppConfig
from django.db.models.signals import post_migrate

def add_default_categories(sender, **kwargs):
    from .models import Category

    # 한글로 작성된 기본 카테고리 데이터 10개
    default_categories = [
        {'name': '전자제품', 'description': '전자 관련 제품'},
        {'name': '사무용품', 'description': '사무실에서 사용하는 용품'},
        {'name': '가구', 'description': '사무용 가구'},
        {'name': '생활용품', 'description': '일상 생활에 필요한 용품'},
        {'name': '식료품', 'description': '음식 및 식료품'},
        {'name': '청소용품', 'description': '청소 및 위생 용품'},
        {'name': '안전용품', 'description': '안전 관련 용품'},
        {'name': '의류', 'description': '복장 및 의류'},
        {'name': '의료용품', 'description': '의료 및 건강 관련 용품'},
        {'name': '공구', 'description': '수리 및 유지보수용 공구'},
    ]

    # 기본 카테고리를 생성
    for category_data in default_categories:
        Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data['description'],
            }
        )

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        post_migrate.connect(add_default_categories, sender=self)