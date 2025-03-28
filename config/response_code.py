from enum import Enum

class ErrorCode(Enum):
    SERVER_ERROR = ("COMMON-500", "서버 내부 오류가 발생했습니다.")
    NOT_FOUND = ("COMMON-404", "페이지를 찾을 수 없습니다.")
    FORBIDDEN = ("COMMON-403", "접근 권한이 없습니다.")
    BAD_REQUEST = ("COMMON-400", "잘못된 요청입니다.")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class SuccessCode(Enum):
    SUCCESS_CREATE = ("SUCCESS-201", "성공적으로 생성되었습니다.")
    SUCCESS_UPDATE = ("SUCCESS-200", "성공적으로 업데이트되었습니다.")
    SUCCESS_DELETE = ("SUCCESS-204", "성공적으로 삭제되었습니다.")
    
    def __init__(self, code, message):
        self.code = code
        self.message = message
