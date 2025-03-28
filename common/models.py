from django.db import models


class CommonModel(models.Model):
    """공통 속성 모델"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # 아래와 같이 abstract = True를 선언하면 Djnaog에서 이 모델을 데이터베이스에 등록하지 않는다.
    class Meta:
        abstract = True
