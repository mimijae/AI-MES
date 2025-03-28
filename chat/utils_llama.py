import json
import time
from django.db import connection
from .system_prompt import get_system_prompt
from langchain_ollama import OllamaLLM
from .custom_log import llama_pretty_log, pretty_error_log


def execute_sql_query(sql_query):
    """생성된 SQL을 실행하고 결과를 반환"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        llama_pretty_log("SQL 실행 결과", f"{result}")
        return result
    except Exception as e:
        pretty_error_log("SQL 실행 오류", f"SQL 쿼리 실행 중 오류: {e}", level="error")
        raise


def llama_generate_sql(question, model_type="llama3.1:8b"):
    """Llama 모델을 사용해 SQL을 생성하는 함수"""
    try:
        start_time = time.time()
        # 모델 URL 매핑
        model_urls = {
            "llama3.1:8b": "http://localhost:11435",
            "llama3.1:70b": "http://localhost:11436",
            "qwen2.5-coder:7b": "http://localhost:11437",
            "qwen2.5-coder:32b": "http://localhost:11438",
            "llama3.2:3b": "http://localhost:11439",
        }

        if model_type not in model_urls:
            error_message = f"지원되지 않는 모델 타입: {model_type}"
            pretty_error_log("모델 설정 오류", error_message, level="error")
            raise ValueError(error_message)

        base_url = model_urls[model_type]
        llm = OllamaLLM(
            model=model_type,
            base_url=base_url,
            temperature=0.7,
        )

        # 프롬프트 생성
        system_prompt = get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]

        # 모델 호출
        generated_sql = llm.invoke(messages)
        elapsed_time = time.time() - start_time
        llama_pretty_log(
            "SQL 생성 완료",
            f"{model_type} 에서 생성된 SQL:\n{generated_sql}\n\n응답 생성에 걸린 시간: {elapsed_time:.2f} 초",
        )

        return generated_sql.strip()

    except Exception as e:
        error_message = f"{model_type} 호출 중 오류 발생: {e}"
        pretty_error_log("모델 호출 오류", error_message, level="error")
        raise Exception(f"{model_type} 호출 실패: {str(e)}")


def llama_generate_response(system_msg, user_input, model_type="llama3.1:8b"):
    """Llama 모델을 사용해 SQL을 생성하는 함수"""
    try:
        start_time = time.time()
        # 모델 URL 매핑
        # model_urls = {
        #     "llama3.1:8b": "http://localhost:11435",
        #     "llama3.1:70b": "http://localhost:11436",
        #     "qwen2.5-coder:7b": "http://localhost:11437",
        #     "qwen2.5-coder:32b": "http://localhost:11438",
        #     "llama3.2:3b": "http://localhost:11439",
        # }

        model_urls = "http://localhost:11435"

        # if model_type not in model_urls:
        #     error_message = f"지원되지 않는 모델 타입: {model_type}"
        #     pretty_error_log("모델 설정 오류", error_message, level="error")
        #     raise ValueError(error_message)

        # base_url = model_urls[model_type]
        base_url = model_urls

        llm = OllamaLLM(
            model=model_type,
            base_url=base_url,
            temperature=0.7,
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_input},
        ]

        # 모델 호출
        response = llm.invoke(messages)
        elapsed_time = time.time() - start_time

        llama_pretty_log(
            "llama 응답 생성 완료",
            f"디코딩된 응답:\n{response}\n\n응답 생성에 걸린 시간: {elapsed_time:.2f} 초",
        )

        return response

    except Exception as e:
        error_message = f"{model_type} 호출 중 오류 발생: {e}"
        pretty_error_log("모델 호출 오류", error_message, level="error")
        raise Exception(f"{model_type} 호출 실패: {str(e)}")
