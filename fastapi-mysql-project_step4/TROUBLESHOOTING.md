# 🛠️ 트러블슈팅 및 이슈 해결 가이드

이 프로젝트를 구축하면서 발생할 수 있는 주요 오류와 해결 방법을 정리했습니다.

---

## 1. 🚨 ModuleNotFoundError: No module named 'app'
**증상:**
`docker-compose logs` 확인 시 FastAPI 컨테이너에서 위 에러가 발생하며 앱이 죽음.

**원인:**
`docker-compose.yml`의 Volume 마운트 경로가 잘못 설정된 경우.
*   **오류 설정:** `- ./app:/app` (컨테이너의 `/app/main.py`가 됨 -> `app.main` 패키지 인식 불가)
*   **올바른 설정:** `- ./app:/app/app` (컨테이너의 `/app/app/main.py`가 됨 -> `app` 패키지 인식 가능)

**해결:**
`docker-compose.yml`의 volumes 섹션을 수정하고 재빌드합니다.
```yaml
volumes:
  - ./app:/app/app
```

---

## 2. 🚨 Pydantic V2 ValidationError (Extra inputs not permitted)
**증상:**
서버 시작 시 `.env` 파일에 있는 환경 변수들이 `Settings` 클래스에 정의되지 않았다며 에러 발생.

**원인:**
Pydantic V2(`pydantic-settings`)는 기본적으로 모델에 정의되지 않은 필드가 입력값으로 들어오면 에러를 발생시킵니다 (`extra='forbid'`). `.env`에는 DB 접속 정보가 있는데 `config.py`에 선언이 안 되어 있어서 발생했습니다.

**해결:**
`app/core/config.py`의 `Settings` 클래스에 `model_config`를 추가하여 정의되지 않은 변수는 무시하도록 설정합니다.
```python
model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore"  # 핵심!
)
```

---

## 3. 🚨 Connection Refused (Nginx 502 Bad Gateway)
**증상:**
`docker-compose up` 직후 `http://localhost` 접속 시 502 에러가 발생하거나, 로그에 `connect() failed`가 뜸.

**원인:**
FastAPI 컨테이너가 완전히 로딩되기 전에 Nginx가 먼저 요청을 보내서 생기는 일시적인 현상입니다. 혹은 FastAPI가 에러로 죽어있을 때도 발생합니다.

**해결:**
1.  FastAPI가 정상적으로 뜰 때까지 잠시 기다립니다 (보통 5~10초).
2.  `docker-compose logs app`으로 파이썬 에러가 없는지 확인합니다.

---

## 4. 🚨 로컬 VS Code에서 파이썬 인터프리터 미인식
**증상:**
Docker로는 잘 돌아가는데, VS Code 에디터 상에서 `import fastapi` 등에 빨간 줄(Warning)이 뜸.

**원인:**
Docker 컨테이너 안에는 라이브러리가 설치되어 있지만, 내 컴퓨터(로컬) 가상환경에는 설치되지 않았기 때문입니다.

**해결:**
로컬에도 가상환경을 만들고 의존성을 설치해줍니다.
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
그 후 VS Code에서 `F1` > `Python: Select Interpreter` > `.venv` 선택.

---

## 5. 🚨 MySQL "Public Key Retrieval is not allowed"
**증상:**
DB 접속 시 보안 관련 에러 발생.

**원인:**
MySQL 8.0 이상에서 기본 인증 플러그인(`caching_sha2_password`) 사용 시 발생하는 보안 옵션 문제입니다.

**해결:**
SQLAlchemy 접속 URL 혹은 드라이버 설정 변경이 필요할 수 있으나, 보통 Docker 환경 변수 `MYSQL_ROOT_PASSWORD` 등을 명확히 주면 해결됩니다. 만약 계속 발생한다면 접속 URL에 `?allowPublicKeyRetrieval=true` 옵션을 붙여야 할 수도 있습니다 (현재 프로젝트에서는 발생하지 않음).
