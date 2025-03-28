import json
import platform
import decimal
import pandas as pd
from datetime import datetime, date
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from io import BytesIO
import base64
import logging
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db.models import Q
from django.db.models.functions import TruncDate
from .models import Chat
from .utils_gpt4 import gpt4_generate_response
from .utils_llama import llama_generate_sql, execute_sql_query, llama_generate_response
from .custom_log import pretty_log, pretty_error_log
from .system_prompt import (
    django_model_prompt_with_language_support,
    get_summarize_data_prompt_with_improvements,
)
from django.conf import settings
from matplotlib import font_manager

logger = logging.getLogger(__name__)  # 운영체제별 폰트 설정

from pathlib import Path
from matplotlib import font_manager, rc
import platform

FONT_PATH = settings.BASE_DIR / "_static/font/NanumFontSetup_OTF_GOTHIC/NanumGothic.otf"

# Matplotlib 폰트 설정
if platform.system() == "Windows":
    font_name = "Malgun Gothic"  # Windows: 맑은 고딕
    print("Windows 환경 - 폰트: 맑은 고딕")
elif platform.system() == "Darwin":  # MacOS
    font_name = "AppleGothic"  # MacOS: 애플 고딕
    print("MacOS 환경 - 폰트: 애플 고딕")
else:
    # Linux: NanumGothic 폰트 적용
    if FONT_PATH.exists():
        font_name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
        print(f"Linux 환경 - 커스텀 폰트: {font_name} ({FONT_PATH})")
    else:
        print(f"Linux 환경 - 폰트 파일 {FONT_PATH}이(가) 존재하지 않습니다.")
        font_name = "DejaVu Sans"  # 예비 기본 폰트

# Matplotlib에 폰트 설정 적용
rc("font", family=font_name)
plt.rcParams["axes.unicode_minus"] = False  # 음수 부호 깨짐 방지



@login_required
def chat_page(request):
    """이전 대화 기록을 날짜별로 불러와 채팅 페이지를 렌더링합니다."""
    chat_history_by_date = (
        Chat.objects.filter(user=request.user)
        .annotate(chat_date=TruncDate("created_at"))
        .order_by("chat_date", "created_at")
    )

    grouped_chat_history = {}
    for chat in chat_history_by_date:
        date = chat.chat_date
        if date not in grouped_chat_history:
            grouped_chat_history[date] = []
        grouped_chat_history[date].append(
            {
                "id": chat.id,
                "prompt": chat.prompt,
                "response": chat.response,
                "table": chat.table,
                "chart": chat.chart,
                "time": chat.created_at.strftime("%p %I:%M")
                .replace("AM", "오전")
                .replace("PM", "오후"),
            }
        )

    return render(
        request, "chat/chat.html", {"grouped_chat_history": grouped_chat_history}
    )


def save_chat(user, prompt, response, table, chart):
    """Chat 모델에 데이터를 저장"""
    Chat.objects.create(
        user=user, prompt=prompt, response=response, table=table, chart=chart
    )


@csrf_exempt
def chat_api(request):
    """사용자의 자연어 요청을 모델로 처리하고, 결과를 반환합니다."""
    if request.method == "POST":
        try:
            # 요청 데이터 파싱
            request_data = json.loads(request.body)
            user_input = request_data.get("user_input")
            model_type = request_data.get("model_type", "").lower().strip()

            pretty_log(model_type, user_input)

            # 모델 타입 확인
            valid_models = [
                "llama3.1:8b",
                "llama3.1:70b",
                "qwen2.5-coder:7b",
                "qwen2.5-coder:32b",
                "llama3.2:3b",
                "gpt-4o",
            ]
            if model_type not in valid_models:
                return JsonResponse(
                    {"response": "지원되지 않는 모델 유형입니다."}, status=400
                )

            # GPT 모델 처리
            if model_type == "gpt-4o":
                try:
                    gpt_response = gpt4_generate_response(
                        django_model_prompt_with_language_support(), user_input
                    )
                    response_data = json.loads(gpt_response)

                    app_name = response_data.get("app")
                    model_name = response_data.get("model")
                    query_condition = response_data.get("query", "")

                    if app_name and model_name:
                        model = apps.get_model(app_name, model_name)
                        queryset = (
                            model.objects.filter(eval(query_condition, {"Q": Q}))
                            if query_condition
                            else model.objects.all()
                        )

                        response_text, table_html, chart_base64 = (
                            format_queryset_results(queryset)
                        )
                        save_chat(
                            request.user,
                            user_input,
                            response_text,
                            table_html,
                            chart_base64,
                        )

                        return JsonResponse(
                            {
                                "response": response_text,
                                "table": table_html,
                                "chart": chart_base64,
                            }
                        )
                    else:
                        return JsonResponse(
                            {"response": "유효하지 않은 요청입니다."}, status=400
                        )

                except json.JSONDecodeError:
                    pretty_error_log(
                        "GPT 처리 오류",
                        f"GPT 응답 처리 중 오류 발생: {gpt_response}",
                        level="error",
                    )
                    return JsonResponse(
                        {"response": "GPT 응답 처리 중 오류가 발생했습니다."},
                        status=400,
                    )
                except Exception as e:
                    pretty_error_log(
                        "GPT 처리 오류", f"GPT 처리 중 오류 발생: {e}", level="error"
                    )
                    return JsonResponse(
                        {"response": "GPT 처리 중 오류가 발생했습니다."}, status=500
                    )

            # Llama 및 Qwen 모델 처리
            else:
                try:
                    generated_sql = llama_generate_sql(user_input, model_type)
                    query_results = execute_sql_query(generated_sql)

                    response_text, table_html, chart_base64 = format_sql_results(
                        query_results
                    )

                    save_chat(
                        request.user,
                        user_input,
                        response_text,
                        table_html,
                        chart_base64,
                    )

                    return JsonResponse(
                        {
                            "response": response_text,
                            "table": table_html,
                            "chart": chart_base64,
                        }
                    )
                except Exception as e:
                    pretty_error_log(
                        "모델 처리 오류",
                        f"{model_type} 처리 중 오류 발생: {e}",
                        level="error",
                    )
                    return JsonResponse(
                        {"response": f"{model_type} 처리 중 오류가 발생했습니다."},
                        status=500,
                    )

        except json.JSONDecodeError:
            return JsonResponse(
                {"response": "요청 형식이 JSON이 아닙니다."}, status=400
            )
        except Exception as e:
            pretty_error_log(
                "알 수 없는 오류", f"알 수 없는 오류 발생: {e}", level="error"
            )
            return JsonResponse(
                {"response": "알 수 없는 오류가 발생했습니다."}, status=500
            )
    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)


def convert_values(x):
    # NaT 값을 None으로 반환하여 오류 방지
    if pd.isnull(x):
        return None
    if isinstance(x, decimal.Decimal):
        return float(x)
    elif isinstance(x, (pd.Timestamp, datetime, date)):
        return x.strftime("%Y-%m-%d %H:%M")
    return x


def format_queryset_results(queryset):
    """Queryset 데이터를 텍스트, 표, 그래프로 변환합니다."""
    if queryset.exists():
        # 데이터 프레임 생성
        df = pd.DataFrame(list(queryset.values()))

        # 모든 데이터를 문자열 또는 숫자로 변환하여 JSON 직렬화 지원
        df = df.applymap(convert_values)

        # GPT 호출 결과 처리
        gpt_response = gpt4_generate_response(
            get_summarize_data_prompt_with_improvements(),
            json.dumps(df.to_dict(orient="records")),
        )

        try:
            # GPT 응답이 문자열로 반환된 경우 JSON으로 파싱
            gpt_data = json.loads(gpt_response)
        except json.JSONDecodeError as e:
            pretty_error_log(
                "GPT 처리 오류",
                f"GPT 응답 처리 중 오류 발생: {gpt_response}",
                level="error",
            )
            return "GPT 응답 처리에 문제가 발생했습니다.", "", ""

        # 결과 처리
        return process_gpt_data(df, gpt_data)

    return "조회 결과가 없습니다.", "", ""


def format_sql_results(sql_results):
    """SQL 쿼리 결과를 텍스트, 표, 그래프로 변환합니다."""
    if sql_results:
        # 데이터 프레임 생성
        df = pd.DataFrame(sql_results)

        # 모든 데이터를 문자열 또는 숫자로 변환하여 JSON 직렬화 지원
        df = df.applymap(convert_values)

        # llama 호출 결과 처리
        gpt4_response = gpt4_generate_response(
            get_summarize_data_prompt_with_improvements(),
            json.dumps(df.to_dict(orient="records")),
        )

        try:
            # GPT 응답이 문자열로 반환된 경우 JSON으로 파싱
            gpt_data = json.loads(gpt4_response)
        except json.JSONDecodeError as e:
            pretty_error_log(
                "GPT 처리 오류",
                f"GPT 응답 처리 중 오류 발생: {gpt4_response}",
                level="error",
            )
            return "GPT 응답 처리에 문제가 발생했습니다.", "", ""

        # 결과 처리
        return process_gpt_data(df, gpt_data)

    return "조회 결과가 없습니다.", "", ""


def process_gpt_data(df, gpt_data):
    """GPT 응답 데이터를 처리하여 텍스트, 테이블, 그래프를 반환합니다."""
    column_translations = gpt_data.get("column_translations", {})
    x_axis_field = gpt_data.get(
        "x_axis_field", df.columns[0] if not df.empty else "unknown"
    )  # 기본값 설정
    x_label = gpt_data.get("x_label", "항목")
    y_label = gpt_data.get("y_label", "값")
    graph_title = gpt_data.get("title", "데이터 항목별 시각화")
    summary_text = gpt_data.get("summary", "")

    # id 및 외래 키 제거
    columns_to_exclude = ["id"] + [col for col in df.columns if col.endswith("_id")]
    df = df.drop(columns=columns_to_exclude, errors="ignore")

    # 생성일 및 수정일 컬럼을 맨 끝으로 이동
    date_columns = [col for col in ["created_at", "updated_at"] if col in df.columns]
    other_columns = [col for col in df.columns if col not in date_columns]
    df = df[other_columns + date_columns]

    # 컬럼명을 번역
    df.rename(columns=column_translations, inplace=True)

    # 요약 설명 생성
    response_text = f"{len(df)}개의 항목이 검색되었습니다.\n\n{summary_text}\n"

    # 테이블 HTML 생성
    table_html = df.to_html(index=False, classes="styled-table", escape=True)

    # 그래프 생성
    chart_base64 = ""
    logger.info(f"데이터프레임 컬럼: {df.columns.tolist()}")
    logger.info(f"GPT x축 필드: {x_axis_field}")
    logger.info(f"숫자 데이터프레임: {df.select_dtypes(include=['number'])}")

    if not df.select_dtypes(include=["number"]).empty and x_axis_field in df.columns:
        fig, ax = plt.subplots()

        x_data = df[x_axis_field]
        y_data = df.select_dtypes(include=["number"]).iloc[:, 0]

        ax.bar(x_data, y_data)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(graph_title)

        for container in ax.containers:
            ax.bar_label(container, label_type="edge")

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

    return response_text, table_html, chart_base64


@csrf_exempt
def chat_by_date_api(request):
    """선택한 날짜의 대화 목록을 반환하는 API"""
    date_str = request.GET.get("date")
    if date_str:
        try:
            # 날짜 형식을 'YYYY-MM-DD'로 변환
            date = datetime.strptime(date_str, "%Y년 %m월 %d일").strftime("%Y-%m-%d")
            logger.info(f"Fetching chat history for date: {date}")

            chats = Chat.objects.filter(
                user=request.user, created_at__date=date
            ).order_by("created_at")
            chat_data = [
                {
                    "prompt": chat.prompt,
                    "response": chat.response,
                    "table": chat.table,
                    "chart": chat.chart,
                    "time": chat.created_at.strftime("%p %I:%M")
                    .replace("AM", "오전")
                    .replace("PM", "오후"),
                }
                for chat in chats
            ]
            return JsonResponse({"chats": chat_data})
        except ValueError:
            pretty_error_log(
                "날짜 형식 오류",
                f"날짜 형식이 잘못되었습니다. 예상 형식: 'YYYY년 MM월 DD일'",
                level="warning",
            )
            return JsonResponse(
                {"error": "Invalid date format. Expected format: 'YYYY년 MM월 DD일'"},
                status=400,
            )

    logger.warning("No date provided in chat_by_date_api.")
    return JsonResponse({"error": "Date parameter is required"}, status=400)
