# 초기 설정
> ## quiz 폴더  
### .env파일 생성
- django key 및 db정보는 별도 파일로 관리
```
SECRET_KEY='django_key'
DB_NAME='db_name'
DB_USER='db_user'
DB_PASSWORD='db_password'
DB_HOST='host'
DB_PORT='port'
```

# API
## 1. account
### 일반사용자 계정 생성
- url

    ```
    account/signup-user/
    ```
- 요청 예시
    ```JSON
    "username": "name",
    "password": "password"
    ```
### 관리자 계정 생성
- url
    ```
    account/signup-admin/
    ```
- 요청 예시
    ```JSON
    "username": "name",
    "password": "password"
    ```
## 2. quiz_manager

### - 생성 (POST)
- url
    ```
    quiz/
    ```
- 요청 예시
    ```JSON
    {
    "title": "퀴즈 제목",
    "questions": [
        {
            "title": "문제1",
            "answer": ["선택지1", "선택지2", "선택지3"],
            "correct_answer": "선택지1"
        },
        {
            "title": "문제2",
            "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "correct_answer": "선택지4"
        }
    ]
    }
    ```

### - 조회 (GET)  
- url
    ```
    quiz/
    ```
- 응답 예시
    ```JSON
    {
    "id" : 0
    "title": "퀴즈 제목",
    "questions": [
        {
            "id" : 0,
            "title": "문제1",
            "answer": ["선택지1", "선택지2", "선택지3"],
            "correct_answer": "선택지1"
        },
        {
            "id" : 1,
            "title": "문제2",
            "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "correct_answer": "선택지4"
        }
    ]
    }
    ```

### - 수정 (PUT/PATCH)
- url
    ```
    quiz/{quiz id}/
    ```
- 요청 예시
    ```JSON
    {
    "title": "퀴즈 제목",
    "questions": [
        {
            "title": "문제1",
            "answer": ["선택지1", "선택지2", "선택지3"],
            "correct_answer": "선택지1"
        },
        {
            "title": "문제2",
            "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "correct_answer": "선택지4"
        }
    ]
    }
    ```

### 삭제 (DELETE)
- url
    ```
    quiz/{quiz id}/
    ```