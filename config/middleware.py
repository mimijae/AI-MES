# middleware.py
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .response_code import ErrorCode
import logging

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        전역 예외를 처리하는 메서드. AJAX 요청과 일반 HTML 요청을 구분하여 처리합니다.
        """
        logger.error(f"Exception occurred: {exception}", exc_info=True)

        # AJAX 요청인 경우 JSON 응답을 반환
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "successFlag": False,
                "code": ErrorCode.SERVER_ERROR.code,
                "message": str(exception),
                "length": 0,
                "data": None
            }, status=500)

        # 일반 HTML 요청인 경우 에러 페이지 렌더링
        return render(request, '500.html', {
            'code': ErrorCode.SERVER_ERROR.code,
            'message': ErrorCode.SERVER_ERROR.message
        }, status=500)
