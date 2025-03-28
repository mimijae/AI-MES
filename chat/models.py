# chat/models.py
from django.db import models
from common.models import CommonModel
from users.models import User

class Chat(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()  # 사용자 프롬프트 저장
    response = models.TextField()  # 봇 응답 저장
    table = models.TextField(null=True, blank=True)  # 테이블 HTML 저장 필드
    chart = models.TextField(null=True, blank=True)  # Base64 인코딩된 차트 저장 필드

    def __str__(self):
        return f"{self.user.username} - {self.prompt[:50]}"
    class Meta:
        db_table = 'chat'
        
