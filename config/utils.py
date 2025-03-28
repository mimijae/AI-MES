# utils.py

from django.http import JsonResponse
from django.shortcuts import render


class CustomResponse:
    def __init__(self, success_flag=True, code=None, message=None, data=None, length=None):
        self.success_flag = success_flag
        self.code = code
        self.message = message
        self.data = data
        self.length = length or (len(data) if data else 0)

    def to_json(self, status=200):
        """
        AJAX 요청에 대한 JSON 응답을 반환
        """
        return JsonResponse({
            "successFlag": self.success_flag,
            "code": self.code,
            "message": self.message,
            "length": self.length,
            "data": self.data
        }, status=status)

    def to_html(self, request, template_name):
        """
        HTML 렌더링 시 불필요한 메타 정보를 제외하고 필요한 데이터만 전달
        """
        return render(request, template_name, {"data": self.data})
