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
    {
        "username": "name",
        "password": "password"
    }
    ```
### 관리자 계정 생성
- url
    ```
    account/signup-admin/
    ```
- 요청 예시
    ```JSON
    {
        "username": "name",
        "password": "password"
    }
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
        "questions_count": 10,
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
        "questions_count": 10,
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
        "questions_count": 10,
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

## 3. quiz_board
### - 관리자용 게시판 설정 (PUT/PATCH)
1시간 간격으로 설정정보를 캐싱 진행  
관리자가 수정한 경우 캐싱정보 갱신
- url
    ```
    /board/setting/1/
    ```
- 요청 예시  
quiz_paging : 퀴즈 목록 페이징 개수. default = 10  
question_paging : 퀴즈 내 문제 페이징 개수. default = 10  
question_random : 퀴즈 내 문제 순서 랜덤 여부. default = False  
choice_random : 문제 선택지 랜덤 여부. default = False
    ```JSON
    {
        "quiz_paging": 10,
        "question_paging": 10,
        "question_random": false,
        "choice_random": false
    }
    ```


### - 퀴즈 목록 조회 (GET)
quiz_id : 질문 정보  
질문 정보의 경우 상세 조회에서만 출력될 수 있도록 설정
- url
    ```
    /board/?page={page_num}
    ```
- 응답 예시
    ```JSON
    {
        "count": 12,
        "next": "/board/?page=2",
        "previous": null,
        "results": [
            {
                "id": 18,
                "title": "퀴즈 제목",
                "questions_count": 10,
                "quiz_id": []
            },
            {
                "id": 17,
                "title": "퀴즈 제목",
                "questions_count": 10,
                "quiz_id": []
            }
    }
    ```

### - 퀴즈 상세 정보 (GET)
- url
    ```
    /board/{quiz_id}/?page={page_num}
    ```
- 응답예시
    ```JSON
    {
        "count": 10,
        "next": "http://127.0.0.1:8000/board/12/?page=2",
        "previous": null,
        "results": {
            "quiz_id": [
                    {
                    "id": 18,
                    "title": "문제2",
                    "answer": [
                        "선택지2",
                        "선택지1",
                        "선택지3",
                        "선택지4"
                        ]
                    },
                    {
                    "id": 18,
                    "title": "문제2",
                    "answer": [
                        "선택지2",
                        "선택지1",
                        "선택지4",
                        "선택지3"
                    ]
                }
            ]
        }
    }
    ```