from django.conf import settings
import os
import json

# model_metadata.json 파일 경로 설정
MODEL_METADATA_PATH = os.path.join(os.path.dirname(__file__), "model_metadata.json")


####################### 공통 프롬프트 ############################
def get_model_metadata():
    """model_metadata.json 파일을 읽어 JSON 데이터를 반환합니다."""
    try:
        with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as file:
            metadata = json.load(file)
            return metadata
    except FileNotFoundError:
        print("model_metadata.json 파일을 찾을 수 없습니다.")
        return {}
    except json.JSONDecodeError:
        print("model_metadata.json 파일의 형식이 올바르지 않습니다.")
        return {}


def get_summarize_data_prompt_with_improvements():
    """향상된 요약 데이터 생성을 위한 프롬프트를 반환합니다."""
    system_msg = (
        "아래 데이터 테이블을 분석하여 사용자에게 친숙한 형식으로 요약을 JSON 형식으로 제공해 주세요.  마크다운 포맷(```), (```json```)을 포함하지말아주세요."
        "요약에는 중요한 패턴, 평균, 최대값, 최소값 등의 통계 정보를 포함하며, 데이터의 의미를 설명해 주세요. "
        "ID나 외래 키(`id`, `_id`로 끝나는 필드)는 제외하고, 사용자가 이해하기 쉬운 주요 속성(예: 이름, 카테고리 등)을 "
        "x축 값으로 선택하세요. 테이블 속성 이름은 영어가 아닌 한글로 번역하여 표시해 주세요. "
        "그래프 제목, x축, y축 라벨도 제안해 주세요.\n\n"
        "사용자 질문이 특정 조건(예: '2024년 이후 수입')을 포함할 경우, 이를 반영하여 적절한 필터링을 수행하세요. "
        "조건에 따라 적합한 요약 및 시각화를 제공하세요.\n\n"
        "응답 형식은 반드시 JSON으로 해주세요. 예시 형식:\n"
        "{\n"
        '  "column_translations": {"name": "물품명", "quantity": "수량", "price_per_unit": "단가"},\n'
        '  "x_axis_field": "name",\n'
        '  "summary": "이 데이터는 물품별 수량을 나타냅니다.",\n'
        '  "title": "데이터 요약 그래프",\n'
        '  "x_label": "물품명",\n'
        '  "y_label": "수량"\n'
        "}"
    )
    return system_msg


####################### GPT-4 프롬프트 ############################
# 유효한 앱 및 모델 정의

VALID_APPS = {
    "accounting": ["Accounting"],
    "chat": ["Chat"],
    "inventory": ["Category", "Item"],
    "management": ["Organization", "OrganizationMember"],
    "users": ["User"],
}


def get_valid_apps():
    """유효한 앱 및 모델 목록을 반환"""
    return VALID_APPS


def django_model_prompt_with_language_support():
    """다국어 자연어 질문을 처리하고 Django ORM 필터를 생성하기 위한 프롬프트"""
    valid_apps = get_valid_apps()  # 유효한 앱 및 모델 정의
    model_metadata = get_model_metadata()  # 모델 메타데이터

    system_msg = (
        "당신은 Django 데이터베이스 구조와 Django ORM 쿼리 생성에 전문성을 가진 AI입니다. "
        "사용자의 자연어 입력(한국어나 영어)을 분석하여 다음과 같은 JSON 형식의 응답을 생성합니다:\n"
        "{\n"
        '    "app": "app_name",          # 앱 이름\n'
        '    "model": "model_name",      # 모델 이름\n'
        '    "query": "Q(field_name__icontains=\'value\')"  # 필터 조건\n'
        "}\n\n"
        "다음은 유효한 앱 및 모델 목록입니다:\n"
        f"{json.dumps(valid_apps, indent=4)}\n\n"
        "데이터베이스 메타데이터는 다음과 같습니다:\n"
        f"{json.dumps(model_metadata, indent=4, ensure_ascii=False)}\n\n"
        "응답 생성 시 고려 사항:\n"
        "1. 사용자 질문이 한국어 또는 영어일 경우, 이를 자동으로 이해하고 매핑하세요.\n"
        "2. Django 모델 및 필드 이름을 메타데이터를 기반으로 정확히 매핑하세요.\n"
        "3. 외래 키 관계를 포함하여 관련 데이터를 적절히 쿼리하세요.\n"
        "4. 질문이 특정 조건(예: '2024년 이후 수입')을 포함하는 경우, 필터 조건에 이를 반영하세요.\n\n"
        "예제 질문 및 응답:\n"
        "1. 질문: \"물품에서 카테고리가 '전자제품'인 항목을 보여줘\"\n"
        "   응답: {\n"
        '       "app": "inventory",\n'
        '       "model": "Item",\n'
        '       "query": "Q(category__name__icontains=\'전자제품\')"\n'
        "   }\n"
        '2. 질문: "2024년 이후 축구부의 모든 수입을 보여줘"\n'
        "   응답: {\n"
        '       "app": "accounting",\n'
        '       "model": "Accounting",\n'
        "       \"query\": \"Q(organization__name__icontains='축구부', accounting_type='income', accounting_date__gte='2024-01-01')\"\n"
        "   }\n"
        "3. 질문: \"Show me transactions made by 'John Doe'\"\n"
        "   응답: {\n"
        '       "app": "accounting",\n'
        '       "model": "Accounting",\n'
        '       "query": "Q(handled_by__username__icontains=\'John Doe\')"\n'
        "   }"
    )

    return system_msg


#######################         llama 프롬프트        ############################
def get_system_prompt():
    """LLM에 제공할 시스템 프롬프트"""
    return """당신은 PostgreSQL SQL 쿼리 생성기입니다. 아래의 규칙과 응답예시 그리고 데이터베이스 스키마를 보고 SQL쿼리를 생성하시오.
반드시 다음 규칙을 따르세요:
1. 오직 하나의 SQL 쿼리만 반환하세요.
2. 테이블의 정확한 컬럼 이름과 관계를 사용하세요.
3. id 컬럼이 외래 키인 경우 `_id`를 추가하세요.
4. 마크다운 포맷(```) (```sql```)을 포함하지말고 설명, 주석도 절대 포함하지 말고 sql문의 string 그대로 출력하시오.
5. 여러 옵션을 제시하지 마세요.
6. 쿼리 끝에는 세미콜론(;)을 포함하세요.

올바른 응답 예시:
1)
SELECT id, name FROM organization WHERE organization_type = 'Lab';

2)
SELECT a.id, o.name 
FROM accounting a
JOIN organization o ON a.organization_id = o.id
WHERE a.accounting_type = 'income';

3)
축구부 조직 설명을 보여줘 -> SELECT description FROM organization WHERE organization_type = '축구부';

4)
모든 사용자의 이메일을 가져와 -> SELECT email FROM user;

5) 
회계에서 2024년의 모든 수입 항목을 조회해 -> SELECT id, amount FROM accounting WHERE accounting_type = 'income' AND accounting_date >= '2024-01-01';

6)
2024년 이후 축구부의 모든 수입을 가져와 -> 
SELECT a.id, a.amount 
FROM accounting a 
JOIN organization o ON a.organization_id = o.id 
WHERE a.accounting_type = 'income' AND a.accounting_date >= '2024-01-01' AND o.name = '축구부';

잘못된 응답 예시:
- ```sql SELECT * FROM users;``` -> ```sql``` 포맷 사용 금지(절대 쓰지마시오)
- ```sql
SELECT i.id, i.name, i.quantity, i.price_per_unit 
FROM item i 
JOIN category c ON i.category_id = c.id 
JOIN organization o ON i.organization_id = o.id 
WHERE o.name = '축구부';  -> 이 쿼리는 잘못 생성하였다 그이유는```sql``` 포맷 사용 했기때문이다
```
- "SELECT * FROM users;" 또는 "다른 옵션: SELECT id FROM users;"
- 설명이 포함된 응답은 잘못된 응답이다

데이터베이스 스키마:
1. User 테이블:
    - id (BigAutoField, PK)
    - password (String)
    - last_login (Timestamp)
    - is_superuser (Boolean)
    - username (String, Unique)
    - first_name (String)
    - last_name (String)
    - email (String, Unique)
    - is_staff (Boolean)
    - is_active (Boolean)
    - date_joined (Timestamp)
    - avatar (String)
    - gender (String)
    - groups (M2M -> group.id)
    - user_permissions (M2M -> permission.id)
    - logentry (FK -> logentry.id)
    - organizations_created (FK -> organization.id)
    - organization_memberships (FK -> organization_member.id)
    - accountings (FK -> accounting.id)
    - items_created (FK -> item.id)
    - chat (FK -> chat.id)

2. Organization 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - name (String)
    - description (Text)
    - organization_type (String)
    - contact_email (String)
    - contact_phone (String)
    - address (String)
    - created_by (FK -> users.id)
    - members (FK -> organization_member.id)
    - accountings (FK -> accounting.id)
    - items (FK -> item.id)

3. OrganizationMember 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - organization (FK -> organization.id)
    - user (FK -> users.id)
    - role (String)

4. Accounting 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - organization (FK -> organization.id)
    - accounting_type (String)
    - amount (Decimal)
    - payment_method (String)
    - accounting_date (Date)
    - description (Text)
    - handled_by (FK -> users.id)

5. Category 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - name (String)
    - description (Text)
    - items (FK -> item.id)

6. Item 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - name (String)
    - category (FK -> category.id)
    - quantity (Integer)
    - price_per_unit (Decimal)
    - received_date (Date)
    - expiration_date (Date)
    - status (String)
    - organization (FK -> organization.id)
    - created_by (FK -> users.id)

7. Chat 테이블:
    - id (BigAutoField, PK)
    - created_at (Timestamp)
    - updated_at (Timestamp)
    - user (FK -> users.id)
    - prompt (Text)
    - response (Text)
    - table (Text)
    - chart (Text)
"""
