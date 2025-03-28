# AI-MES-SmartFactory

## 1. 프로젝트 개요

이 프로젝트는 제조 실행 시스템(MES, Manufacturing Execution System)을 Django와 PostgreSQL 기반으로 구축하고, 스마트 팩토리 구조를 구현하는 것을 목표로 합니다. 사용자는 채팅을 통해 데이터를 입력하고, AI를 활용해 SQL을 생성하여 데이터베이스에서 데이터를 조회, 분석한 후 표, 그래프, 글 등 다양한 형식으로 응답을 받게 됩니다. 이를 통해 사용자에게 유동적으로 정보를 제공하는 시스템을 구축합니다. 최종적으로 LLAMA 3.1 8B를 로컬 서버에 설치해, AI 기반 데이터 분석 및 학습을 통해 스마트 팩토리의 효율성을 극대화합니다.

## 2. 프로젝트 구동

- 가상환경 생성
```bash
python -m venv venv
```

- 가상환경 접속
```bash
venv/Scripts/activate 
```

- 프로젝트에서 사용하는 라이브러리 목록 자동설치
```bash
pip install -r requirements.txt
```

- 모델 마이그레이트
```bash
python manage.py migrate
```

- 웹 프로젝트 실행
```bash
python manage.py runserver
```

*오류
```
venv/Scripts/activate : 이 시스템에서 스크립트를 실행할 수 없으므로 \venv\Scripts\Activate.ps1 파일을 로드할 수 없습니다. 자세한 내용은 about_Execution_Po 
licies(https://go.microsoft.com/fwlink/?LinkID=135170)를 참조하십시오.
위치 줄:1 문자:1
+ venv/Scripts/activate
+ ~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : 보안 오류: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess

이렇게 나올 경우
```
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


## 3. 라마 모델 변경 경로
- AI-MES-SmartFactory/chat/llama_model.py 의 model_id 변수의 값을 변경하면 됨
# AI-MES
