import logging

logger = logging.getLogger(__name__)  # 운영체제별 폰트 설정


def pretty_log(model_type, user_input):
    """모델과 사용자 입력을 보기 좋게 로그 출력"""
    separator = "-" * 60
    header = f"\033[1;34m{separator}\n[ 💻 모델 요청 로그 ]\n{separator}\033[0m"  # 파란색 헤더
    body = (
        f"\033[1;33m모델 선택:\033[0m {model_type}\n"
        f"\033[1;32m사용자 입력:\033[0m {user_input}"
    )
    footer = f"\033[1;34m{separator}\033[0m"  # 파란색 푸터

    # Print to console
    print(f"{header}\n{body}\n{footer}")

    # Log to file
    logger.info(f"\n{header}\n{body}\n{footer}")


def pretty_error_log(context, message, level="info"):
    """에러 로그를 보기 좋게 출력"""
    separator = "\033[1;31m" + "-" * 60 + "\033[0m"  # 빨간색 구분선
    header = f"\033[1;31m[ ❌ {context} ]\033[0m"  # 빨간색 제목
    footer = separator

    body = f"\033[1;33m{message}\033[0m"  # 노란색 메시지

    # 터미널 출력
    print(f"{separator}\n{header}\n{body}\n{footer}")

    # 로그 메시지 작성
    log_message = f"{separator}\n{header}\n{body}\n{footer}"
    if level == "error":
        logger.error(log_message)
    elif level == "warning":
        logger.warning(log_message)
    else:
        logger.info(log_message)


def llama_pretty_log(title, content, level="info"):
    """Llama 로그를 보기 좋게 출력"""
    separator = "\033[1;36m" + "-" * 60 + "\033[0m"  # 청록색 구분선
    header = f"\033[1;36m[ 📝 {title} ]\033[0m"  # 청록색 제목
    footer = separator

    body = f"\033[1;37m{content}\033[0m"  # 흰색 본문

    # 터미널 출력
    print(f"{separator}\n{header}\n{body}\n{footer}")

    # 로그 메시지 작성
    log_message = f"{separator}\n{header}\n{body}\n{footer}"
    if level == "info":
        logger.info(log_message)
    elif level == "error":
        logger.error(log_message)
    elif level == "warning":
        logger.warning(log_message)


def gpt_pretty_log(title, content, level="info"):
    """GPT 로그를 보기 좋게 출력"""
    separator = "\033[1;35m" + "-" * 60 + "\033[0m"  # 보라색 구분선
    header = f"\033[1;35m[ 🧠 {title} ]\033[0m"  # 보라색 제목
    footer = separator

    body = f"\033[1;32m{content}\033[0m"  # 초록색 본문

    # 터미널 출력
    print(f"{separator}\n{header}\n{body}\n{footer}")

    # 로그 메시지 작성
    log_message = f"{separator}\n{header}\n{body}\n{footer}"
    if level == "info":
        logger.info(log_message)
    elif level == "error":
        logger.error(log_message)
    elif level == "warning":
        logger.warning(log_message)
