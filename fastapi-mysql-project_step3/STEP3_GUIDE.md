# 🚀 Step 3: DB 모델링 및 SQLAlchemy 비동기 연동

이 문서는 **Step 3** 단계에서 추가된 DB 관련 설정과 모델링에 대해 설명합니다.

## 1. 주요 변경 사항

### A. 비동기 DB 세션 (`app/db/session.py`)
*   **`create_async_engine`**: 동기식(`Blocking`)이 아닌 비동기식(`Non-blocking`)으로 DB와 통신하는 엔진을 생성했습니다. 이는 고성능 API 서버의 핵심입니다.
*   **`get_db`**: API 요청(Request)마다 DB 세션을 열고, 응답(Response) 후 닫아주는 함수입니다.

### B. 데이터 모델 (`app/models/`)
SQLAlchemy를 사용하여 두 개의 테이블을 정의했습니다.
1.  **`items`**: 제목, 설명 등을 저장하는 일반 데이터용.
2.  **`uploaded_files`**: 파일명, 경로, 크기 등 파일 정보를 저장하는 메타데이터용.

### C. 데이터 검증 (`app/schemas/`)
Pydantic V2를 사용하여 API 입출력 데이터를 엄격하게 관리합니다.
*   **`ItemCreate`**: 사용자가 보낼 데이터 (title 필수).
*   **`ItemResponse`**: 서버가 돌려줄 데이터 (id 포함).

### D. 자동 테이블 생성 (`app/main.py`)
*   FastAPI의 **`lifespan`** 기능을 사용하여, 서버가 켜질 때 자동으로 `init_tables()`를 호출합니다.
*   이로 인해 DB에 접속해서 `CREATE TABLE IF NOT EXISTS ...` 쿼리를 날려 테이블을 만듭니다.

---

## 2. 실행 및 확인 방법

### 컨테이너 재실행
새로운 라이브러리나 설정은 없지만, 코드 변경 사항을 확실히 적용하기 위해 재시작을 권장합니다.

```bash
cd fastapi-mysql-project_step3
docker-compose down
docker-compose up -d --build
```

### 로그 확인
DB 테이블이 정상적으로 생성되었는지 로그로 확인합니다.

```bash
docker-compose logs -f app
```
로그 중에 **`✅ Database tables created successfully.`** 라는 메시지와 함께 `CREATE TABLE ...` SQL 문들이 보이면 성공입니다.

### MySQL 직접 접속 확인 (Optional)
컨테이너에 들어가서 실제로 테이블이 생겼는지 볼 수 있습니다.

```bash
docker exec -it fastapi_db mysql -u myuser -p
# Password 입력: mypassword
USE myproject;
SHOW TABLES;
# items, uploaded_files 테이블이 보이면 성공!
```

---

## 3. 다음 단계 (Step 4 Preview)
이제 DB 테이블까지 준비되었습니다. 다음 단계에서는:
1.  **CRUD API 구현:** 실제 `items` 테이블에 데이터를 넣고 빼는 API 만들기.
2.  **파일 업로드 API 구현:** 파일을 받아 `uploads` 폴더에 저장하고, 정보를 `uploaded_files` 테이블에 기록하기.
를 진행하게 됩니다.
