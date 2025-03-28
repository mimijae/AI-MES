# utils_gpt4.py
import json
import time
from openai import OpenAI
from django.conf import settings
import os
from .system_prompt import get_model_metadata
from .custom_log import gpt_pretty_log, pretty_error_log
import logging

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=settings.OPENAI_API_KEY)
engine = "gpt-4"


logger = logging.getLogger(__name__)  # 운영체제별 폰트 설정


def gpt4_generate_response(system_msg, user_input):
    """GPT-4 모델로 시스템 메시지와 사용자 입력을 처리해 응답을 생성하는 함수"""
    try:
        start_time = time.time()

        # 시스템 메시지 및 사용자 입력 로그
        logger.info("GPT-4 응답 생성 시작")

        completion = client.chat.completions.create(
            model=engine,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_input},
            ],
            temperature=0.1,
        )

        # 응답 디코딩
        response = completion.choices[0].message.content
        elapsed_time = time.time() - start_time

        # 생성 완료 로그
        gpt_pretty_log(
            "GPT-4 응답 생성 완료",
            f"디코딩된 응답:\n{response}\n\n응답 생성에 걸린 시간: {elapsed_time:.2f} 초",
        )
        return response

    except Exception as e:
        error_message = f"GPT-4 API 호출 중 오류 발생: {e}"
        pretty_error_log("GPT-4 API 오류", error_message, level="error")
        return None
